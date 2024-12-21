from celery import chain, group

from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import User
from chemicals.tasks import post_chemical
from .util.util import generate_random_alphanumeric_sequence
from .serializers import PDFSerializer
from .tasks import (
    extract_chemical_from_pdf,
    monitor_json_file,
    load_chemical_from_json
)

FILE_RANDOM_NAME_SIZE = 10

# Create your views here.
class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = PDFSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_files = serializer.validated_data['pdf_files']
            email = serializer.validated_data['email']
            
            temp_files = []
            
            try:
                user = User.objects.get(email=email)
                
                for file in uploaded_files:
                    # Salva cada arquivo como temporário
                    pdf_file_path = default_storage.save(f"tmp_pdfs/{generate_random_alphanumeric_sequence(FILE_RANDOM_NAME_SIZE)}.pdf", file)

                    #file_url = default_storage.url(file_path)
                    temp_files.append(pdf_file_path)
                    
                    # Enfileira para processamento
                    chain(
                        extract_chemical_from_pdf.s(pdf_file_path),
                        monitor_json_file.s(),
                        load_chemical_from_json.s(),
                        lambda chemical_list: group(post_chemical.s(chemical, user.id) for chemical in chemical_list)
                    )()
                    
                    #extract_chemical_from_pdf.apply_async(args=[user.id, pdf_file_path], priority=10)

                return Response(
                    {"message": f"{len(uploaded_files)} files enqueued for processing."},
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                # Garantia de limpeza em caso de erro
                for temp_file in temp_files:
                    default_storage.delete(temp_file)
                
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)