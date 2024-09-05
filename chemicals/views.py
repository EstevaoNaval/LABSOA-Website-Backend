from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, permissions, filters
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ChemicalAutocompleteSerializer, ChemicalSerializer, ChemicalSummarySerializer
from .models import Chemical

from .filters import (
    ChemicalAdvancedSearchFilter,
    ChemicalAutocompleteSearchFilter,
    ChemicalSimpleSearchFilter
)

CACHE_TTL = 60 * 60 * 2 # 2 horas

class ChemicalAdvancedSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    filterset_class = ChemicalAdvancedSearchFilter
    
class ChemicalAdvancedSearchSummaryView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSummarySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    filterset_class = ChemicalAdvancedSearchFilter

class ChemicalSimpleSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    filterset_class = ChemicalSimpleSearchFilter

class ChemicalSimpleSearchSummaryView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSummarySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    filterset_class = ChemicalSimpleSearchFilter

class AutocompleteSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalAutocompleteSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ChemicalAutocompleteSearchFilter

class ChemicalReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    ordering = ['api_id']
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)   

class ChemicalSummaryReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSummarySerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'api_id', 
        'physical_properties__count_h_bond_acceptor',
        'physical_properties__count_h_bond_donor',
        'physical_properties__count_heavy_atom',
        'physical_properties__molecular_weight',
        'physicochemical_properties__tpsa',
        'physical_properties__count_rotatable_bond',
        'partition_coefficients__jplogp',
        'physical_properties__mp_lower_bound',
        'physical_properties__mp_upper_bound',
        'created_at'
    ]
    ordering = ['api_id']
    permission_classes = [permissions.AllowAny]
    
    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ChemicalAdminViewSet(viewsets.ModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['api_id']
    ordering = ['api_id']
    permission_classes = [permissions.IsAuthenticated]