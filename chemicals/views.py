from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, permissions, filters
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    ChemicalAutocompleteSerializer, 
    ChemicalSerializer, 
    ChemicalSummarySerializer, 
    ChemicalPropListSerializer
)
from .models import Chemical
from .pagination import PropListPagination

from .filters import (
    ChemicalAdvancedSearchFilter,
    ChemicalAutocompleteSearchFilter,
)

CACHE_TTL = 60 * 60 * 2 # 2 horas

ORDERING_FIELDS_LIST = [
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

class ChemicalPropListView(ListAPIView):
    pagination_class = PropListPagination
    serializer_class = ChemicalPropListSerializer
    ordering = ['api_id']
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ChemicalAdvancedSearchFilter
    
    
    def get_queryset(self):
        queryset = Chemical.objects.all()
        
        queryset = self.filter_queryset(queryset)
        
        return queryset.values(
            'physical_properties__count_h_bond_acceptor',
            'physical_properties__count_h_bond_donor',
            'physical_properties__count_heavy_atom',
            'physical_properties__molecular_weight',
            'physicochemical_properties__tpsa',
            'physical_properties__count_rotatable_bond',
            'partition_coefficients__jplogp',
            'physical_properties__mp_lower_bound',
            'physical_properties__mp_upper_bound',
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginated_queryset = self.paginate_queryset(queryset)

        # Organiza os dados em listas separadas para cada propriedade
        h_bond_acceptor_list = [item['physical_properties__count_h_bond_acceptor'] for item in paginated_queryset if item['physical_properties__count_h_bond_acceptor'] is not None]
        h_bond_donor_list = [item['physical_properties__count_h_bond_donor'] for item in paginated_queryset if item['physical_properties__count_h_bond_donor'] is not None]
        heavy_atom_list = [item['physical_properties__count_heavy_atom'] for item in paginated_queryset if item['physical_properties__count_heavy_atom'] is not None]
        molecular_weight_list = [item['physical_properties__molecular_weight'] for item in paginated_queryset if item['physical_properties__molecular_weight'] is not None]
        tpsa_list = [item['physicochemical_properties__tpsa'] for item in paginated_queryset if item['physicochemical_properties__tpsa'] is not None]
        rotatable_bond_list = [item['physical_properties__count_rotatable_bond'] for item in paginated_queryset if item['physical_properties__count_rotatable_bond'] is not None]
        jplogp_list = [item['partition_coefficients__jplogp'] for item in paginated_queryset if item['partition_coefficients__jplogp'] is not None]
        mp_lower_bound_list = [item['physical_properties__mp_lower_bound'] for item in paginated_queryset if item['physical_properties__mp_lower_bound'] is not None]
        mp_upper_bound_list = [item['physical_properties__mp_upper_bound'] for item in paginated_queryset if item['physical_properties__mp_upper_bound'] is not None]
        #publication_date_list = [item['publication_date'] for item in paginated_queryset if item['publication_date'] is not None]

        response_data = {
            'h_bond_acceptor': h_bond_acceptor_list,
            'h_bond_donor': h_bond_donor_list,
            'heavy_atom': heavy_atom_list,
            'molecular_weight': molecular_weight_list,
            'tpsa': tpsa_list,
            'rotatable_bond': rotatable_bond_list,
            'jplogp': jplogp_list,
            'mp_lower_bound': mp_lower_bound_list,
            'mp_upper_bound': mp_upper_bound_list,
            #'publication_date': publication_date_list,
        }

        return self.get_paginated_response(response_data)

class ChemicalSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ORDERING_FIELDS_LIST
    filterset_class = ChemicalAdvancedSearchFilter
    
class ChemicalSearchSummaryView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSummarySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ORDERING_FIELDS_LIST
    filterset_class = ChemicalAdvancedSearchFilter

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
    ordering_fields = ORDERING_FIELDS_LIST
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
    ordering_fields = ORDERING_FIELDS_LIST
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