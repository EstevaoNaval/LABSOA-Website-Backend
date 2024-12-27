import requests
from io import BytesIO

from django.conf import settings

from celery import shared_task

@shared_task(
    name='chemicals.tasks.django_tasks_patch_conformation', 
    bind=True,
    queue='django_tasks',
    priority=10,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def patch_conformation(self, chemical_id: str, conformations: list[str]):
    files = {}
    
    for idx, conf_data in enumerate(conformations):
        files[f"conformations[{idx}][conf_file]"] = (
            f"conf_{idx}.sdf", 
            BytesIO(conf_data.encode('utf-8')), # Conteúdo do arquivo em memória
            "chemical/x-mdl-sdfile" # Tipo MIME
        )
    
    r = requests.patch(
        url=settings.API_BASE_URL+f"/api/chemicals/admin/{chemical_id}/",
        files=files,
        headers={
            'Authorization': 'Bearer {}'.format(settings.CELERY_AUTH_TOKEN)
        }
    )
    
    r.raise_for_status()

@shared_task(
    name='chemicals.tasks.django_tasks_patch_depiction', 
    bind=True, 
    queue='django_tasks',
    priority=10,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def patch_depiction(self, chemical_id, depiction: str):
    files = {}
    
    files['depiction_image'] = (
        'depiction_image.svg',
        BytesIO(depiction.encode('utf-8')),
        "image/svg+xml"
    )
    
    r = requests.patch(
        url=settings.API_BASE_URL+f"/api/chemicals/admin/{chemical_id}/",
        files=files,
        headers={
            'Authorization': 'Bearer {}'.format(settings.CELERY_AUTH_TOKEN)
        }
    )
    
    r.raise_for_status()

@shared_task(
    name='chemicals.tasks.django_tasks_post_chemical', 
    bind=True, 
    queue='django_tasks',
    priority=10,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 60},
    retry_backoff=True,
    task_reject_on_worker_lost=True
)
def post_chemical(self, chemical: dict, user_id: int):
    conformations = chemical.pop('conformation', [])
    chem_depiction_image = chemical.pop('chem_depiction_image', '')
    
    chemical['user'] = user_id    
    
    r = requests.post(
        url=settings.API_BASE_URL+"/api/chemicals/admin/",
        json=chemical,
        headers={
            'Authorization': 'Bearer {}'.format(settings.CELERY_AUTH_TOKEN)
        }
    )
    
    r.raise_for_status()
    
    chemical_id = r.json().get("api_id")
    
    patch_conformation.apply_async(args=[chemical_id, conformations], priority=10)
    patch_depiction.apply_async(args=[chemical_id, chem_depiction_image], priority=10)