from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        validators = [
            RegexValidator(
                regex=r'^[A-Za-z0-9_-]+$',
                message="Username must contain only letters, digits, hyphens (-), or underscores (_)."
            )
        ]
    )
    password = models.CharField(
        max_length=100,
        validators = [
            MinLengthValidator(
                limit_value=10,
                message="The password must be at least 10 characters long."
            )
        ]
    )

    # Definindo o email como identificador para login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']  # Campos obrigatórios para o superusuário

    def __str__(self):
        return self.email
