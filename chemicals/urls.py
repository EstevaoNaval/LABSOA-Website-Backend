from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChemicalReadOnlyViewSet, 
    ChemicalAdminViewSet, 
    AutocompleteSearchView, 
    ChemicalSimpleSearchView,
    ChemicalAdvancedSearchView
)

router = DefaultRouter()
router.register(r'', ChemicalReadOnlyViewSet, basename='chemical')
router.register(r'admin', ChemicalAdminViewSet, basename='admin-chemical')

urlpatterns = [
    path(route='autocomplete/', view=AutocompleteSearchView.as_view(), name='autocomplete-search'),
    path(route='search/', view=ChemicalSimpleSearchView.as_view(), name='simple-search'),
    path(route='advanced/', view=ChemicalAdvancedSearchView.as_view(), name='advanced-search'),
    path('', include(router.urls))
]