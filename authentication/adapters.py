# myapp/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """
        Retorna a URL de confirmação de e-mail.
        Substitua 'frontend_url' pela URL da sua aplicação front-end.
        """
        frontend_url = f"{settings.FRONTEND_URL}{settings.FRONTEND_EMAIL_CONFIRMATION_ENDPOINT}"
        return f"{frontend_url}?key={emailconfirmation.key}"
