from django.http import FileResponse
from django.db.models.manager import BaseManager

from chemicals.factories.export_service_factory import ExportServiceFactory
from chemicals.models import Chemical

class BaseExportView:
    content_type_mapping = {
        'csv': 'text/csv',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xls': 'application/vnd.ms-excel',
        'ods': 'application/vnd.oasis.opendocument.spreadsheet',
        'json': 'application/json',
        'html': 'text/html'
    }
    default_format = 'csv' 

    def validate_format(self, export_format):
        if export_format not in self.content_type_mapping:
            raise ValueError(f"Unsupported format: {export_format}")

    def generate_file_response(self, queryset: BaseManager[Chemical], export_format: str, filename: str):
        
        export_service = ExportServiceFactory.get_service(export_format)
        
        file_buffer = export_service.export(queryset)
        
        response = FileResponse(
            file_buffer,
            content_type=self.content_type_mapping[export_format],
            as_attachment=True,
            filename=filename
        )
        
        return response
