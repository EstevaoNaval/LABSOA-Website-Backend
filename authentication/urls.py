from django.urls import path, include

from knox import views as knox_views

from dj_rest_auth.views import (
    PasswordChangeView, 
    PasswordResetView, 
    PasswordResetConfirmView, 
    UserDetailsView
)

from .views import (
    UserConfirmEmailView,
    LoginView
)

urlpatterns = [
    # URLs para registro e autenticação
    path(
        'register/account-confirm-email/',
        UserConfirmEmailView.as_view(),
        name='account_email_verification_sent'
    ),
    path('register/', include('dj_rest_auth.registration.urls')),
    
    # Gerenciamento de usuários pelo dj-rest-auth
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path(
        'password/reset/confirm/<uidb64>/<token>/', 
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    
    path('user/', UserDetailsView.as_view(), name='user_details')
]
