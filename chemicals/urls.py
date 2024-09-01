from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChemicalReadOnlyViewSet, 
    ChemicalAdminViewSet, 
    AutocompleteSearchView,
    ChemicalSummaryReadOnlyViewSet, 
    ChemicalSimpleSearchView,
    ChemicalSimpleSearchSummaryView,
    ChemicalAdvancedSearchView,
    ChemicalAdvancedSearchSummaryView
)

router = DefaultRouter()
router.register(r'summary', ChemicalSummaryReadOnlyViewSet, basename='chemical-summary')
router.register(r'admin', ChemicalAdminViewSet, basename='admin-chemical')
router.register(r'', ChemicalReadOnlyViewSet, basename='chemical')

urlpatterns = [
    path(route='autocomplete/', view=AutocompleteSearchView.as_view(), name='autocomplete-search'),
    path(route='search/', view=ChemicalSimpleSearchView.as_view(), name='simple-search'),
    path(route='advanced/', view=ChemicalAdvancedSearchView.as_view(), name='advanced-search'),
    path(route='search/summary/', view=ChemicalSimpleSearchSummaryView.as_view(), name='simple-search-summary'),
    path(route='advanced/summary/', view=ChemicalAdvancedSearchSummaryView.as_view(), name='advanced-search-summary'),
    path('', include(router.urls))
]