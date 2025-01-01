from io import BytesIO
from abc import ABC, abstractmethod

from django.db.models.manager import BaseManager

from chemicals.resources import ChemicalResource
from chemicals.models import Chemical


class ExportFileService(ABC):
    @staticmethod
    @abstractmethod
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        pass

class XlsxExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('xlsx'))
        bytes_buf.seek(0)
        
        return bytes_buf
        
class XlsExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('xls'))
        bytes_buf.seek(0)
        
        return bytes_buf
        
class OdsExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('ods'))
        bytes_buf.seek(0)
        
        return bytes_buf

class CsvExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('csv').encode())
        bytes_buf.seek(0)
        
        return bytes_buf
    
class JsonExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('json').encode())
        bytes_buf.seek(0)
        
        return bytes_buf

class HtmlExportService(ExportFileService):
    def export(queryset: BaseManager[Chemical], *args, **kwargs) -> BytesIO:       
        bytes_buf = BytesIO()
        
        resource = ChemicalResource()
        tablib_dataset = resource.export(queryset)
        
        bytes_buf.write(tablib_dataset.export('html').encode())
        bytes_buf.seek(0)
        
        return bytes_buf