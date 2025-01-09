'''import re

from django.contrib.auth import get_user_model
from rest_framework import serializers, status

from .models import User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate_username(self, value):
        # Validar o formato do username usando regex
        if not re.match(r'^[A-Za-z0-9_-]+$', value):
            raise serializers.ValidationError(
                {"username": "username must contain only letters, digits, hyphens (-), or underscores (_)."},
                code=status.HTTP_400_BAD_REQUEST
            )
        return value
    
    def validate(self, data):
        # Valida se a senha e a confirmação de senha coincidem
        if 'password' in data:
            if data['password'] != data.get('password_confirmation'):
                raise serializers.ValidationError(
                    {"password": "password and password confirmation do not match."}, 
                    code=status.HTTP_400_BAD_REQUEST
                )
        
        return data
    
    def create(self, validated_data):
        # Cria o usuário usando o método create_user, que já lida com a hash da senha
        validated_data.pop('password_confirmation')
        
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password_confirmation', None)
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        return user'''