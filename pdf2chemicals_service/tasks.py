import os
from celery import shared_task
from pathlib import Path
import json
from dotenv import load_dotenv

from django.conf import settings
from django.core.files.storage import default_storage

from pdf2chemicals_service.util.util import generate_random_alphanumeric_sequence
from pdf2chemicals_service.monitor import monitor_directory
from libs.pdf2chemicals.pdf2chemicals import main
from chemicals.tasks import post_chemical

# Function to load environment variables from the .env file
def load_environment_variables():
    """
    Loads the environment variables from the .env file.
    Returns: JAVA_HOME and CONDA_ENV.
    """
    load_dotenv()
    java_home = os.getenv("JAVA_HOME")
    conda_env = os.getenv("CONDA_ENV")
    return java_home, conda_env

# Function to load the PBS template and replace variables
def load_and_replace_template(job_id, template_path, java_home, conda_env, pdf2chemicals_path, pdf_path, output_dir, json_prefix):
    """
    Loads the PBS template and replaces the variables with the correct values.
    
    Parameters:
    - job_id: PBS job id.
    - template_path: Path to the template file.
    - java_home: JAVA_HOME path.
    - conda_env: Conda environment name.
    - pdf2chemicals_path: Path to the pdf2chemicals script.
    - pdf_path: Path to the PDF to be processed.
    - output_dir: Directory where the output will be saved.
    - json_prefix: Prefix for the output JSON file.
    
    Returns:
    - The script content with the replaced variables.
    """
    # Load the template content
    with open(template_path, 'r') as file:
        template_content = file.read()

    # Replace the variables in the template
    script_content = template_content.replace("{{job_id}}", job_id)
    script_content = template_content.replace("{{JAVA_HOME}}", java_home)
    script_content = script_content.replace("{{conda_env}}", conda_env)
    script_content = script_content.replace("{{pdf2chemicals_path}}", pdf2chemicals_path)
    script_content = script_content.replace("{{pdf_path}}", pdf_path)
    script_content = script_content.replace("{{output_dir}}", output_dir)
    script_content = script_content.replace("{{json_prefix}}", json_prefix)
    
    return script_content

# Function to generate a script name with a random suffix
def generate_script_name(base_name="pbs_script"):
    """
    Generates a unique PBS script name with a random suffix.
    Returns: The script name with the random suffix.
    """
    PBS_SCRIPT_RANDOM_SUFFIX_SIZE = 10
    
    random_suffix = generate_random_alphanumeric_sequence(PBS_SCRIPT_RANDOM_SUFFIX_SIZE)
    return f"{base_name}_{random_suffix}.pbs"

# Function to save the generated script in the media directory
def save_script(script_content, script_name):
    """
    Saves the PBS script content to a file inside MEDIA_ROOT.
    
    Parameters:
    - script_content: The content of the PBS script.
    - script_name: The name of the file where the script will be saved.
    """
    # Directory to save PBS scripts
    pbs_scripts_dir = os.path.join(settings.MEDIA_ROOT, 'pbs_scripts')
    
    # Ensure the directory exists, otherwise create it
    os.makedirs(pbs_scripts_dir, exist_ok=True)

    # Full path to the file where the script will be saved
    script_path = os.path.join(pbs_scripts_dir, script_name)

    # Save the script to the file
    with open(script_path, 'w') as file:
        file.write(script_content)
    
    print(f"Script saved as: {script_path}")

def get_pdf2chemicals_pbs_template_path():
    return os.path.join(os.path.dirname(__file__), 'pbs_template', 'pdf2chemicals_pbs_template.pbs')

def get_pdf2chemicals_path():
    return os.path.join(settings.BASE_DIR, 'libs', 'pdf2chemicals', 'pdf2chemicals.py')

def generate_pbs_script(pdf_path, output_dir, json_prefix):
    """
    Generates a PBS script for chemical processing by replacing the necessary variables.
    
    Parameters:
    - template_path: Path to the PBS template file.
    - pdf2chemicals_path: Path to the pdf2chemicals script.
    - pdf_path: Path to the PDF to be processed.
    - output_dir: Directory where the results will be saved.
    - json_prefix: Prefix for the output JSON file.
    """
    JOB_ID_SIZE = 10
    
    # Load environment variables
    java_home, conda_env = load_environment_variables()

    job_id = generate_random_alphanumeric_sequence(JOB_ID_SIZE)

    # Generate the script name with a random suffix
    script_name = generate_script_name()

    template_path = get_pdf2chemicals_pbs_template_path()

    pdf2chemicals_path = get_pdf2chemicals_path()

    # Load the template and replace the variables
    script_content = load_and_replace_template(
        job_id,
        template_path, 
        java_home, 
        conda_env, 
        pdf2chemicals_path, 
        pdf_path, 
        output_dir, 
        json_prefix
    )

    # Save the generated script in the media directory
    save_script(script_content, script_name)

@shared_task(
    name='pdf2chemicals_service.tasks.heavy_tasks_extract_chemical_from_pdf', 
    bind=True,  
    acks_late=True,
    queue='heavy_tasks',
    priority=1,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def extract_chemical_from_pdf(self, pdf_path: str):
    JSON_FILENAME_LENGTH = 10
    
    json_dir = settings.MEDIA_ROOT / 'json'
    json_filename = generate_random_alphanumeric_sequence(JSON_FILENAME_LENGTH) + ".json"
    json_path = Path(json_dir) / json_filename
    
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    
    generate_pbs_script(
        absolute_pdf_path,
        json_path,
        '--json'
    )
    
    return json_path
    
    #TODO Chamar o job para executar o pdf2chemicals
    
    #monitor_for_json.delay(json_dir, json_filename, user_id)
    
    #default_storage.delete(pdf_path)
    
    #for chemical_data in chemical_data_list:
    #    post_chemical.apply_async(args=[chemical_data, user_id], priority=10)
        
    #del chemical_data_list
    
@shared_task(
    name='pdf2chemicals_service.tasks.light_tasks_monitor_for_json', 
    bind=True,  
    acks_late=True,
    queue='light_tasks',
    priority=1,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def monitor_json_file(self, json_file_path: Path):
    """
    Task to monitor the directory and detect the JSON file.
    """
    monitor_directory(json_file_path.parent, json_file_path.name)
    
    return json_file_path
    
@shared_task(
    name='chemicals.tasks.light_task_load_chemical_from_json', 
    bind=True, 
    queue='light_tasks',
    priority=10,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def load_chemical_from_json(self, json_file_path: Path):
    with open(json_file_path, mode='r') as json_file:
        chemical_list = json.load(json_file)
        
    return chemical_list