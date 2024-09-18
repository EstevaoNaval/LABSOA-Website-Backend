from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PropListPagination(PageNumberPagination):
    page_size = 1000  # Defina o tamanho padrão da página
    page_size_query_param = 'page_size'  # Permite que o usuário altere o tamanho da página
    max_page_size = 1000  # Define o limite máximo para o tamanho da página
