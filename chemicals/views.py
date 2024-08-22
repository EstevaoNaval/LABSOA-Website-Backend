from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, permissions, filters
from rest_framework.generics import ListAPIView

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ChemicalAutocompleteSerializer, ChemicalSerializer
from .models import Chemical
from .utils import RepresentationDetector

from .factories.search_service_factory import SearchServiceFactory
from .factories.search_context_factory import SearchContextFactory

from .filters import ChemicalAdvancedSearchFilter

CACHE_TTL = 60 * 60 * 6 # 6 horas

class ChemicalAdvancedSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ChemicalAdvancedSearchFilter


class ChemicalSimpleSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        similarity_threshold = float(self.request.query_params.get('similarity_threshold', 0.51))
        
        if query:
            representation_type = RepresentationDetector.detect_type(query)
            search_type = self.determine_search_type(representation_type)
            
            service = SearchServiceFactory.get_service(representation_type)
            
            context = SearchContextFactory.get_context(service, search_type)
            
            self.queryset = context.search(query, self.queryset, similarity_threshold=similarity_threshold)
            
            return self.queryset
        
        return Chemical.objects.none()
    
    def determine_search_type(self, representation_type):
        search_map = {
            'smiles': 'exact',
            'api_id': 'exact',
            'inchi': 'exact',
            'inchi_key': 'exact',
            'formula': 'exact',
            'smarts': 'substructure',
            'fulltext': 'similarity'
        }
        
        return search_map.get(representation_type, 'exact')

class AutocompleteSearchView(ListAPIView):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalAutocompleteSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        
        if query:
            if RepresentationDetector.detect_type(query) == 'smiles':
                similarity_threshold = .85
                representation_type = 'smiles'
            else:
                similarity_threshold = .51
                representation_type = 'fulltext'
            
            search_type = self.determine_search_type(representation_type)
            
            service = SearchServiceFactory.get_service(representation_type)
            
            context = SearchContextFactory.get_context(service, search_type)
            
            self.queryset = context.search(query, self.queryset, similarity_threshold=similarity_threshold)
            
            return self.queryset
            
        return Chemical.objects.none()
    
    def determine_search_type(self, representation_type):
        search_map = {
            'smiles': 'similarity',
            'fulltext': 'similarity'
        }
        
        return search_map.get(representation_type, 'similarity')

class ChemicalReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['api_id']
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