import logging

import requests
from celery import shared_task
from celery.utils.log import get_logger

from django.conf import settings
from django.core.files.storage import default_storage

from pdf2chemicals.pdf2chemicals.pdf2chemicals import main

logger = get_logger(__name__)

@shared_task(bind=True)
def extract_chemical_from_pdf(self, pdf_path: str):
    logger.info("Task is running")
    
    pdf_name = pdf_path.split('/')[-1]
    
    chemical_data_list = main(pdf_path)
    
    default_storage.delete(pdf_name)
    
    url = settings.API_BASE_URL+"/api/chemicals/admin/"
    
    headers = {'Content-Type': 'application/json'}
    
    for chemical_data in chemical_data_list:
        response = requests.post(
            url=url,
            headers=headers,
            json=chemical_data
        )