from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer

User = get_user_model()

# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    ordering_fields = ['first_name']
    ordering = ['first_name']
    
    def get_queryset(self):
        # Você pode personalizar a consulta, por exemplo, retornar apenas o próprio usuário
        return super().get_queryset().filter(username=self.request.user.username)
    
    def get_permissions(self):
        if self.action == 'create':  # Permite acesso aberto para registro de novos usuários
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        # Obtém o usuário que está tentando ser deletado
        user = self.get_object()

        # Garante que o usuário autenticado só delete a própria conta
        if request.user != user:
            return Response(
                {"detail": "Você não tem permissão para deletar este usuário."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Deleta o usuário
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)