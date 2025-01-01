from io import BytesIO

from django.db.models.manager import BaseManager

from chemicals.services.export_services import ExportFileService
from chemicals.models import Chemical

class ExportFileContext:
    def __init__(self, export_file_service = ExportFileService):
        self.__export_file_service = export_file_service
        
    def set_export_excel_service(self, export_file_service: ExportFileService):
        self.__export_file_service = export_file_service
    
    def export(self, queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        if not self.__export_file_service:
            raise ValueError('A export service must be set before exporting chemicals.')
        
        return self.__export_file_service.export(queryset, *args, **kwargs)