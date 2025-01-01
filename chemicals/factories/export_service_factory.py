from chemicals.contexts.export_file_context import ExportFileContext
from chemicals.services.export_services import (
    CsvExportService,
    XlsxExportService,
    XlsExportService,
    OdsExportService,
    JsonExportService,
    HtmlExportService
)

class ExportServiceFactory:
    service_mapping = {
        'csv': CsvExportService,
        'xlsx': XlsxExportService,
        'xls': XlsExportService,
        'ods': OdsExportService,
        'json': JsonExportService,
        'html': HtmlExportService
    }

    @staticmethod
    def get_service(file_format):
        service_class = ExportServiceFactory.service_mapping.get(file_format)
        
        if service_class is None:
            raise ValueError(f"Format '{file_format}' is not supported.")
        
        return ExportFileContext(service_class)
