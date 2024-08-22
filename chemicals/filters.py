import django_filters
from .models import Chemical
from .utils import RepresentationDetector
from .factories.search_service_factory import SearchServiceFactory
from .factories.search_context_factory import SearchContextFactory

class ChemicalAdvancedSearchFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_representation_and_search_type', required=False)
    
    class Meta:
        model = Chemical
        fields = {
            'api_id': ['exact']
        }
        
    def filter_by_representation_and_search_type(self, queryset, name, value):
        representation_type = self.request.query_params.get('representation_type', None)
        representation_type = representation_type if representation_type is not None else RepresentationDetector.detect_type(value)
        search_type = self.request.query_params.get('search_type', 'exact')
        threshold = float(self.request.query_params.get('similarity_threshold', .51))
         
        try:
            service = SearchServiceFactory.get_service(representation_type)
            context = SearchContextFactory.get_context(service, search_type)
            
            queryset = context.search(value, queryset, similarity_threshold=threshold)
            
            return queryset
        except ValueError as e:
            return queryset.none()