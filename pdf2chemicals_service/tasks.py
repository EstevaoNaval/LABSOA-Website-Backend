import os
from celery import shared_task
import json
import subprocess
from celery import chain, group

from django.conf import settings

from pdf2chemicals_service.util.celery import ChainedTask
from user.models import User
from pdf2chemicals_service.util.util import generate_random_alphanumeric_sequence
from chemicals.tasks import post_chemical
from .util.util import file_exists
from .cluster import (
    ResourceUnavailable,
    ClusterNodeManager, 
    generate_pbs_script, 
    is_pbs_job_completed
)

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_extract_and_save_chemicals_from_pdf', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    autoretry_for=(Exception,),
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def extract_and_save_chemicals_from_pdf(self, *args, **kwargs):
    user = User.objects.get(email=kwargs['email'])
    
    # Definindo o workflow
    workflow = chain(
        send_pdf2chemicals_hpc_task.s(pdf_path=kwargs['pdf_path']),
        monitor_pdf2chemicals_job.s(),
        load_chemical_from_json.s(),
        process_chemical_list.s(user.id)
    )
    
    # Aplicando o workflow com link_error
    workflow.apply_async(link_error=handle_pdf2chemicals_task_error.s(
        pdf_path=kwargs['pdf_path'],
        email=kwargs['email']
    ))

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.handle_pdf2chemicals_task_error',
    bind=True,
    acks_late=True,
    queue='pdf2chemicals_tasks'
)
def handle_pdf2chemicals_task_error(self, *args, **kwargs):
    # Extraindo os parâmetros necessários de kwargs
    email = kwargs.get('email')
    pdf_path = kwargs.get('pdf_path')

    # Tentando novamente a tarefa original com os parâmetros corretos
    extract_and_save_chemicals_from_pdf.apply_async(
        kwargs={
            'email': email,
            'pdf_path': pdf_path
        },
        countdown=60 * 5  # Waits 5 minutes to retry.
    )

@shared_task(
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_process_chemical_list', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def process_chemical_list(chemical_list, user_id):
    return group(post_chemical.s(chemical, user_id) for chemical in chemical_list)

@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_send_pdf2chemicals_hpc_task', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def send_pdf2chemicals_hpc_task(self, *args, **kwargs):
    JSON_FILENAME_LENGTH = 10
    
    json_dir = os.path.join(settings.MEDIA_ROOT, 'json')
    json_filename = generate_random_alphanumeric_sequence(JSON_FILENAME_LENGTH) + ".json"
    json_path = os.path.join(json_dir, json_filename)
    json_prefix = f"--json --json-filename {json_filename}"
    
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, kwargs['pdf_path'])
    
    cluster_node_manager = ClusterNodeManager()
    
    node_name = cluster_node_manager.get_free_gpu_node()
    
    if node_name == '':
        raise ResourceUnavailable("No pbs node is available at the moment.")
    
    script_path = generate_pbs_script(
        pdf_path=absolute_pdf_path,
        output_dir=json_dir,
        json_prefix=json_prefix,
        node_name=node_name
    )
    
    cmd = f'su - {os.getenv("TORQUE_USER")} -c "{os.getenv("TORQUE_HOME")}/bin/qsub {script_path}"'
    
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=False
    )
    
    if result.returncode != 0:
        raise subprocess.CalledProcessError('Job was not received in the HPC cluster.')
    
    job_id = result.stdout.strip()
    
    cluster_node_manager.mark_node_as_busy(node_name, job_id)
    
    return {
        'job_id': job_id, 
        'node_name': node_name, 
        'json_path': json_path
    } 
    
@shared_task(
    base=ChainedTask,
    name='pdf2chemicals_service.tasks.pdf2chemicals_tasks_monitor_pdf2chemicals_job', 
    bind=True,  
    acks_late=True,
    queue='pdf2chemicals_tasks',
    priority=1,
    max_retries=None,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def monitor_pdf2chemicals_job(self, *args, **kwargs):
    """
    Task to monitor the directory and detect the JSON file.
    """
    print(kwargs)
    
    if not is_pbs_job_completed(kwargs['job_id']):
        self.retry()
    
    cluster_node_manager = ClusterNodeManager()
    
    cluster_node_manager.mark_node_as_free(kwargs['node_name'])
    
    if file_exists(kwargs['json_path']):
        return {
            'json_path': kwargs['json_path']
        }
    
    raise FileExistsError("Json file not found. HPC cluster job executed unsuccessfully.")
    
@shared_task(
    base=ChainedTask,
    name='chemicals.tasks.pdf2chemicals_tasks_load_chemical_from_json', 
    bind=True, 
    queue='pdf2chemicals_tasks',
    priority=10,
    autoretry_for=(Exception,),
    max_retries=5,
    default_retry_delay=60 * 2, # Waits 2 minutes to execute 
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def load_chemical_from_json(self, *args, **kwargs):
    with open(kwargs['json_path'], mode='r') as json_file:
        chemical_list = json.load(json_file)
        
    return chemical_list