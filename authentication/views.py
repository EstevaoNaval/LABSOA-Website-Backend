from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from dj_rest_auth.registration.views import VerifyEmailView

from knox.views import LoginView as KnoxLoginView

class UserConfirmEmailView(VerifyEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        # Substitua pelo URL do seu front-end
        redirect_url = f"{settings.FRONTEND_HOST}{settings.FRONTEND_EMAIL_CONFIRMATION_ENDPOINT}"
        return HttpResponseRedirect(redirect_url)

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        login(request, user)
        
        response = super(LoginView, self).post(request, format=None)
        
        if response.status_code == 200:
            user = request.user
            if not user.emailaddress_set.filter(verified=True).exists():
                return Response({"error": "Email not verified"}, status=400)
        
        return response