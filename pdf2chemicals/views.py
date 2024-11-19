import os

from django.core.files.temp import NamedTemporaryFile

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import PDFSerializer
from .tasks import extract_chemical_from_pdf

# Create your views here.
class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = PDFSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_files = serializer.validated_data['pdf_files']
            temp_files = []
            
            try:
                for file in uploaded_files:
                    # Salva cada arquivo como temporário
                    temp_file = NamedTemporaryFile(delete=False, suffix=".pdf")
                    temp_file.write(file.read())
                    temp_file.close()
                    temp_files.append(temp_file.name)

                    # Enfileira para processamento
                    extract_chemical_from_pdf.delay(temp_file.name)

                return Response(
                    {"message": f"{len(temp_files)} files enqueued for processing."},
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                # Garantia de limpeza em caso de erro
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)