from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChemicalPropListView,
    ChemicalReadOnlyViewSet, 
    ChemicalAdminViewSet, 
    AutocompleteSearchView,
    ChemicalSummaryReadOnlyViewSet,
    ChemicalSearchView,
    ChemicalSearchSummaryView
)

router = DefaultRouter()
router.register(r'summary', ChemicalSummaryReadOnlyViewSet, basename='chemical-summary')
router.register(r'admin', ChemicalAdminViewSet, basename='admin-chemical')
router.register(r'', ChemicalReadOnlyViewSet, basename='chemical')

urlpatterns = [
    path(route='prop-list/', view=ChemicalPropListView.as_view(), name='prop-list'),
    path(route='autocomplete/', view=AutocompleteSearchView.as_view(), name='autocomplete-search'),
    path(route='search/', view=ChemicalSearchView.as_view(), name='search'),
    path(route='search/summary/', view=ChemicalSearchSummaryView.as_view(), name='search-summary'),
    path('', include(router.urls))
]