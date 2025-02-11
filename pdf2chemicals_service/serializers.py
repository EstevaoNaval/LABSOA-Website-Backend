from pyfsig import find_matches_for_file_header

from django_clamd.validators import validate_file_infection

from rest_framework import serializers


class PDFSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_blank=False)
    pdf_files = serializers.ListField(
        child=serializers.FileField(validators=[validate_file_infection]),
        allow_empty=False,
        error_messages={
            'not_a_list': 'Expected a list of files.',
            'empty': 'The list of files cannot be empty.'
        }
    )
    
    def _has_pdf_file_extension_signature(self, file) -> bool:
        file_signatures = self._get_file_signatures(file)
        
        for signature in file_signatures:
            if signature.as_dict()['file_extension'] == 'pdf':
                return True
        
        return False
    
    def _get_file_signatures(self, file):
        # Usar diretamente o arquivo recebido (em memória)
        file.seek(0)
        file_header = file.read(32)
        file.seek(0)
            
        matches = find_matches_for_file_header(file_header=file_header)
        
        return matches
    
    def validate_pdf_files(self, value):
        FILE_MAX_SIZE = 50 * 1024 * 1024 # 50 MB
        
        for file in value:
            if not file.name.endswith(".pdf") or not self._has_pdf_file_extension_signature(file):
                raise serializers.ValidationError("The uploaded files must be in PDF file format.")

            if file.size > FILE_MAX_SIZE: # Files with size greater than 50MB are not allowed.
                raise serializers.ValidationError(f"{file.name} exceeds the size limit of 50 MB.")
        
        return value