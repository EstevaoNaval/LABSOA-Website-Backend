from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PDFUploadView
)

urlpatterns = [
    path('submit/', PDFUploadView.as_view(), name='pdf2chemicals-submit')
]