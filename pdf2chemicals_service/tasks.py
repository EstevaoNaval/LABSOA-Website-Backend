import os
import requests

from django.conf import settings
from django.core.files.storage import default_storage

from celery import shared_task

from libs.pdf2chemicals.pdf2chemicals import main

@shared_task(bind=True, max_retries=3, default_retry_delay=60, acks_late=True)
def extract_chemical_from_pdf(self, user_id: int, pdf_path: str):
    absolute_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    
    chemical_data_list = main(absolute_pdf_path)
    
    default_storage.delete(pdf_path)
    
    for chemical_data in chemical_data_list:
        conf_files = chemical_data.pop('conformation', [])
        
        chemical_data['user'] = user_id
        
        headers = {
            'Authorization': 'Bearer {}'.format(settings.CELERY_AUTH_TOKEN)
        }
        
        requests.post(
            url=settings.API_BASE_URL+"/api/chemicals/admin/",
            json=chemical_data,
            headers=headers
        )