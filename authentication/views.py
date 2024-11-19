from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from rest_framework import permissions, status

class EmailLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        User = get_user_model()

        try:
            user = User.objects.get(email=data.get('email', None))
        except User.DoesNotExist:
            return JsonResponse({"email": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(data.get('password', None)):
            login(request, user)
            return super(EmailLoginView, self).post(request, format=None)

        return JsonResponse({"password": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)