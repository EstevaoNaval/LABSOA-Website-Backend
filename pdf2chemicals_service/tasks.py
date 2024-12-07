import os
from celery import shared_task

from chemicals.tasks import post_chemical

from django.conf import settings
from django.core.files.storage import default_storage

from libs.pdf2chemicals.pdf2chemicals import main

@shared_task(
    name='pdf2chemicals_service.tasks.heavy_task_extract_chemical_from_pdf', 
    bind=True, 
    max_retries=5, 
    default_retry_delay=60, 
    acks_late=True,
    queue='heavy_tasks',
    priority=1
)
def extract_chemical_from_pdf(self, user_id: int, pdf_path: str):
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    
    chemical_data_list = main(absolute_pdf_path)
    
    default_storage.delete(pdf_path)
    
    for chemical_data in chemical_data_list:
        post_chemical.apply_async(args=[chemical_data, user_id], priority=10)
        
    del chemical_data_list