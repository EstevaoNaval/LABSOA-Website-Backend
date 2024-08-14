from chemicals.models import Chemical
from .serializers import ChemicalAutocompleteSerializer, ChemicalSerializer
from .models import Chemical
from .utils import detect_representation
from .services.chemical_search import (
    ChemicalSMILESSearch,
    ChemicalFullTextSearch,
    ChemicalSMARTSSearch,
    ChemicalFormulaSearch,
    ChemicalInchiKeySearch,
    ChemicalInchiSearch,
)
from .services.chemical_search_context import (
    ChemicalSimilaritySearchContext, 
    ChemicalExactSearchContext, 
    ChemicalSubstructureSearchContext
)

from rest_framework import viewsets, permissions, filters
from rest_framework.generics import ListAPIView


class ChemicalAdvancedSearchView(ListAPIView):
    pass

class ChemicalSimpleSearchView(ListAPIView):
    serializer_class = ChemicalSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        
        if query:
            queryset = Chemical.objects.all()
            
            exact_search_context = ChemicalExactSearchContext()
            similarity_search_context = ChemicalSimilaritySearchContext()
            substructure_search_context= ChemicalSubstructureSearchContext()
            
            chem_type_repr = detect_representation(query)
            
            if chem_type_repr == 'smiles':
                exact_search_context.set_chemical_exact_search(ChemicalSMILESSearch)
                queryset = exact_search_context.exact_search(query, queryset)
            elif chem_type_repr == 'inchi':
                exact_search_context.set_chemical_exact_search(ChemicalInchiSearch)
                queryset = exact_search_context.exact_search(query, queryset)
            elif chem_type_repr == 'inchi_key':
                exact_search_context.set_chemical_exact_search(ChemicalInchiKeySearch)
                queryset = exact_search_context.exact_search(query, queryset)
            elif chem_type_repr == 'formula':
                exact_search_context.set_chemical_exact_search(ChemicalFormulaSearch)
                queryset = exact_search_context.exact_search(query, queryset)
            elif chem_type_repr == 'smarts':
                substructure_search_context.set_chemical_substructure_search(ChemicalSMARTSSearch)
                queryset = substructure_search_context.substructure_search(query, queryset)
            else:
                similarity_thereshold = self.request.query_params.get('similarity_thereshold', .45)
                similarity_search_context.set_chemical_similarity_search(ChemicalFullTextSearch)
                queryset = similarity_search_context.similarity_search(query, queryset, similarity_thereshold)    
            
            return queryset
        
        return Chemical.objects.none()

class AutocompleteSearchView(ListAPIView):
    serializer_class = ChemicalAutocompleteSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')

        if query: 
            queryset = Chemical.objects
            
            chem_type_repr = detect_representation(query)
            
            similarity_search_context = ChemicalSimilaritySearchContext()
            
            if chem_type_repr == 'smiles':
                similarity_thereshold = self.request.query_params.get('similarity_thereshold', .85)
            
                similarity_search_context.set_chemical_similarity_search(ChemicalSMILESSearch)
            else:
                similarity_thereshold = self.request.query_params.get('similarity_thereshold', .45)
                
                similarity_search_context.set_chemical_similarity_search(ChemicalFullTextSearch)
            
            queryset = similarity_search_context.similarity_search(query, queryset, similarity_thereshold)
            
            return queryset
        
        return Chemical.objects.none()

class ChemicalReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['api_id']
    ordering = ['api_id']
    permission_classes = [permissions.AllowAny]
    
class ChemicalAdminViewSet(viewsets.ModelViewSet):
    queryset = Chemical.objects.all()
    serializer_class = ChemicalSerializer
    lookup_field = 'api_id'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['api_id']
    ordering = ['api_id']
    permission_classes = [permissions.IsAuthenticated]