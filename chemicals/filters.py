import django_filters
from .models import Chemical
from .utils import RepresentationDetector, CitationDetector
from .factories.search_service_factory import SearchServiceFactory
from .factories.citation_search_service_factory import CitationSearchServiceFactory
from .factories.search_context_factory import SearchContextFactory
from .services.search_services import LiteratureTitleSearchService
from typing import Final

FULLTEXT_SIMILARITY_SEARCH_THRESHOLD: Final[float] = .51
CHEMICAL_REPRESENTATION_SIMILARITY_SEARCH_THRESHOLD: Final[float] = .85

class ChemicalAutocompleteSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_representation_and_search_type', required=True)
    
    class Meta:
        model = Chemical
        fields = []
        
    def filter_by_representation_and_search_type(self, queryset, name, value):
        representation_type = 'smiles' if RepresentationDetector.detect_type(value) == 'smiles' else 'fulltext'
        
        similarity_threshold = CHEMICAL_REPRESENTATION_SIMILARITY_SEARCH_THRESHOLD if representation_type == 'smiles' else FULLTEXT_SIMILARITY_SEARCH_THRESHOLD
        
        search_type = self.determine_search_type(representation_type)
        
        service = SearchServiceFactory.get_service(representation_type)
        context = SearchContextFactory.get_context(service, search_type)
        
        queryset = context.search(value, queryset, similarity_threshold=similarity_threshold)
        
        return queryset
    
    def determine_search_type(self, representation_type):
        search_map = {
            'smiles': 'similarity',
            'fulltext': 'similarity'
        }
        
        return search_map.get(representation_type, 'similarity')
        
class ChemicalAdvancedSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_representation_and_search_type')
    citation = django_filters.CharFilter(method='fiter_by_citation')
    
    # Model Literature
    doi = django_filters.CharFilter(field_name='literature__doi', lookup_expr='iexact')
    title = django_filters.CharFilter(field_name='literature__title', method='filter_by_title')
    publication_date = django_filters.DateFromToRangeFilter(field_name='literature__publication_date')

    # Model PhysicalProperty
    molecular_weight__gte = django_filters.NumberFilter(field_name='physical_properties__molecular_weight', lookup_expr='gte')
    molecular_weight__lte = django_filters.NumberFilter(field_name='physical_properties__molecular_weight', lookup_expr='lte')
    
    volume__gte = django_filters.NumberFilter(field_name='physical_properties__volume', lookup_expr='gte')
    volume__lte = django_filters.NumberFilter(field_name='physical_properties__volume', lookup_expr='lte')
    
    count_atom__gte = django_filters.NumberFilter(field_name='physical_properties__count_atom', lookup_expr='gte')
    count_atom__lte = django_filters.NumberFilter(field_name='physical_properties__count_atom', lookup_expr='lte')
    
    count_heteroatom__gte = django_filters.NumberFilter(field_name='physical_properties__count_heteroatom', lookup_expr='gte')
    count_heteroatom__lte = django_filters.NumberFilter(field_name='physical_properties__count_heteroatom', lookup_expr='lte')
    
    count_heavy_atom__gte = django_filters.NumberFilter(field_name='physical_properties__count_heavy_atom', lookup_expr='gte')
    count_heavy_atom__lte = django_filters.NumberFilter(field_name='physical_properties__count_heavy_atom', lookup_expr='lte')
    
    count_aromatic_heavy_atom__gte = django_filters.NumberFilter(field_name='physical_properties__count_aromatic_heavy_atom', lookup_expr='gte')
    count_aromatic_heavy_atom__lte = django_filters.NumberFilter(field_name='physical_properties__count_aromatic_heavy_atom', lookup_expr='lte')
    
    count_rotatable_bond__gte = django_filters.NumberFilter(field_name='physical_properties__count_rotatable_bond', lookup_expr='gte')
    count_rotatable_bond__lte = django_filters.NumberFilter(field_name='physical_properties__count_rotatable_bond', lookup_expr='lte')
    
    count_h_bond_acceptor__gte = django_filters.NumberFilter(field_name='physical_properties__count_h_bond_acceptor', lookup_expr='gte')
    count_h_bond_acceptor__lte = django_filters.NumberFilter(field_name='physical_properties__count_h_bond_acceptor', lookup_expr='lte')
    
    count_h_bond_donor__gte = django_filters.NumberFilter(field_name='physical_properties__count_h_bond_donor', lookup_expr='gte')
    count_h_bond_donor__lte = django_filters.NumberFilter(field_name='physical_properties__count_h_bond_donor', lookup_expr='lte')
    
    count_ring__gte = django_filters.NumberFilter(field_name='physical_properties__count_ring', lookup_expr='gte')
    count_ring__lte = django_filters.NumberFilter(field_name='physical_properties__count_ring', lookup_expr='lte')
    
    count_carbon__gte = django_filters.NumberFilter(field_name='physical_properties__count_carbon', lookup_expr='gte')
    count_carbon__lte = django_filters.NumberFilter(field_name='physical_properties__count_carbon', lookup_expr='lte')
    
    mp_lower_bound__gte = django_filters.NumberFilter(field_name='physical_properties__mp_lower_bound', lookup_expr='gte')
    mp_upper_bound__lte = django_filters.NumberFilter(field_name='physical_properties__mp_upper_bound', lookup_expr='lte')
    
    state_of_matter = django_filters.CharFilter(field_name='physical_properties__state_of_matter', lookup_expr='iexact')
    
    color = django_filters.CharFilter(field_name='physical_properties__color', lookup_expr='iexact')
    
    color_hexadecimal = django_filters.CharFilter(field_name='physical_properties__color_hexadecimal', lookup_expr='iexact')
    
    # Model PhysicochemicalProperty
    fraction_csp3__gte = django_filters.NumberFilter(field_name='physicochemical_properties__fraction_csp3', lookup_expr='gte')
    fraction_csp3__lte = django_filters.NumberFilter(field_name='physicochemical_properties__fraction_csp3', lookup_expr='lte')
    
    molar_refractivity__gte = django_filters.NumberFilter(field_name='physicochemical_properties__molar_refractivity', lookup_expr='gte')
    molar_refractivity__lte = django_filters.NumberFilter(field_name='physicochemical_properties__molar_refractivity', lookup_expr='lte')
    
    tpsa__gte = django_filters.NumberFilter(field_name='physicochemical_properties__tpsa', lookup_expr='gte')
    tpsa__lte = django_filters.NumberFilter(field_name='physicochemical_properties__tpsa', lookup_expr='lte')
    
    # Model PartitionCoefficient
    wildman_crippen_logp__gte = django_filters.NumberFilter(field_name='partition_coefficients__wildman_crippen_logp', lookup_expr='gte')  
    wildman_crippen_logp__lte = django_filters.NumberFilter(field_name='partition_coefficients__wildman_crippen_logp', lookup_expr='lte')
    
    xlogp__gte = django_filters.NumberFilter(field_name='partition_coefficients__xlogp', lookup_expr='gte')
    xlogp__lte = django_filters.NumberFilter(field_name='partition_coefficients__xlogp', lookup_expr='lte')
    
    jplogp__gte = django_filters.NumberFilter(field_name='partition_coefficients__jplogp', lookup_expr='gte')
    jplogp__lte = django_filters.NumberFilter(field_name='partition_coefficients__jplogp', lookup_expr='lte')
    
    mouriguchi_logp__gte = django_filters.NumberFilter(field_name='partition_coefficients__mouriguchi_logp', lookup_expr='gte')
    mouriguchi_logp__lte = django_filters.NumberFilter(field_name='partition_coefficients__mouriguchi_logp', lookup_expr='lte')
    
    # Model Solubility
    esol_logs__gte = django_filters.NumberFilter(field_name='solubilities__esol_logs', lookup_expr='gte')
    esol_logs__lte = django_filters.NumberFilter(field_name='solubilities__esol_logs', lookup_expr='lte')
    
    filter_it_logs__gte = django_filters.NumberFilter(field_name='solubilities__filter_it_logs', lookup_expr='gte')
    filter_it_logs__lte = django_filters.NumberFilter(field_name='solubilities__filter_it_logs', lookup_expr='lte')
    
    # Model QsarScore
    qed_score__gte = django_filters.NumberFilter(field_name='qsar_scores__qed_score', lookup_expr='gte')
    qed_score__lte = django_filters.NumberFilter(field_name='qsar_scores__qed_score', lookup_expr='lte')
    
    synthetic_accessibility_score__gte = django_filters.NumberFilter(field_name='qsar_scores__synthetic_accessibility_score', lookup_expr='gte')
    synthetic_accessibility_score__lte = django_filters.NumberFilter(field_name='qsar_scores__synthetic_accessibility_score', lookup_expr='lte')
    
    natural_product_score__gte = django_filters.NumberFilter(field_name='qsar_scores__natural_product_score', lookup_expr='gte')
    natural_product_score__lte = django_filters.NumberFilter(field_name='qsar_scores__natural_product_score', lookup_expr='lte')
    
    # Model DrugLikeRule
    count_lipinski_violation__gte = django_filters.NumberFilter(field_name='druglike_rules__count_lipinski_violation', lookup_expr='gte')
    count_lipinski_violation__lte = django_filters.NumberFilter(field_name='druglike_rules__count_lipinski_violation', lookup_expr='lte')
    
    count_ghose_violation__gte = django_filters.NumberFilter(field_name='druglike_rules__count_ghose_violation', lookup_expr='gte')
    count_ghose_violation__lte = django_filters.NumberFilter(field_name='druglike_rules__count_ghose_violation', lookup_expr='lte')
    
    count_veber_violation__gte = django_filters.NumberFilter(field_name='druglike_rules__count_veber_violation', lookup_expr='gte')
    count_veber_violation__lte = django_filters.NumberFilter(field_name='druglike_rules__count_veber_violation', lookup_expr='lte')
    
    count_egan_violation__gte = django_filters.NumberFilter(field_name='druglike_rules__count_egan_violation', lookup_expr='gte')
    count_egan_violation__lte = django_filters.NumberFilter(field_name='druglike_rules__count_egan_violation', lookup_expr='lte')
    
    count_muegge_violation__gte = django_filters.NumberFilter(field_name='druglike_rules__count_muegge_violation', lookup_expr='gte')
    count_muegge_violation__lte = django_filters.NumberFilter(field_name='druglike_rules__count_muegge_violation', lookup_expr='lte')
    
    # Model Pharmacokinetics
    gastrointestinal_absorption = django_filters.BooleanFilter(field_name='pharmacokinetics__gastrointestinal_absorption')
    
    blood_brain_barrier_permeation = django_filters.BooleanFilter(field_name='pharmacokinetics__blood_brain_barrier_permeation')
    
    # Model P450Inhibition
    cyp1a2_inhibitor = django_filters.BooleanFilter(field_name='p450_inhibitors__cyp1a2_inhibitor')
    
    cyp2c9_inhibitor = django_filters.BooleanFilter(field_name='p450_inhibitors__cyp2c9_inhibitor')
    
    cyp2c19_inhibitor = django_filters.BooleanFilter(field_name='p450_inhibitors__cyp2c19_inhibitor')
    
    cyp2d6_inhibitor = django_filters.BooleanFilter(field_name='p450_inhibitors__cyp2d6_inhibitor')
    
    cyp3a4_inhibitor = django_filters.BooleanFilter(field_name='p450_inhibitors__cyp3a4_inhibitor')
    
    # Model UndesirableSubstructureAlert
    count_pains_alert__gte = django_filters.NumberFilter(field_name='undesirable_substructure_alerts__count_pains_alert', lookup_expr='gte')
    count_pains_alert__lte = django_filters.NumberFilter(field_name='undesirable_substructure_alerts__count_pains_alert', lookup_expr='lte')
    
    count_brenk_alert__gte = django_filters.NumberFilter(field_name='undesirable_substructure_alerts__count_brenk_alert', lookup_expr='gte')
    count_brenk_alert__lte = django_filters.NumberFilter(field_name='undesirable_substructure_alerts__count_brenk_alert', lookup_expr='lte') 
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Chemical
        fields = []
        
    def filter_by_representation_and_search_type(self, queryset, name, value):
        if self.request and hasattr(self.request, 'query_params'):
            params = self.request.query_params
        else:
            params = self.data
        
        representation_type = params.get('representation_type', '')
        representation_type = representation_type if representation_type != '' else RepresentationDetector.detect_type(value)
        
        search_type = params.get('search_type', '')
        search_type = search_type if search_type != '' else self._determine_search_type(representation_type)
        
        similarity_threshold = CHEMICAL_REPRESENTATION_SIMILARITY_SEARCH_THRESHOLD if representation_type == 'smiles' else FULLTEXT_SIMILARITY_SEARCH_THRESHOLD
        threshold = float(params.get('similarity_threshold', similarity_threshold))
         
        try:
            service = SearchServiceFactory.get_service(representation_type)
            context = SearchContextFactory.get_context(service, search_type)
            
            queryset = context.search(value, queryset, similarity_threshold=threshold)
            
            return queryset
        except ValueError as e:
            return queryset.none()
    
    def fiter_by_citation(self, queryset, name, value):
        if self.request and hasattr(self.request, 'query_params'):
            params = self.request.query_params
        else:
            params = self.data
        
        citation_type = params.get('citation_type', '')
        citation_type = citation_type if citation_type != '' else CitationDetector.detect_type(value)
        
        similarity_threshold = float(params.get('similarity_threshold', FULLTEXT_SIMILARITY_SEARCH_THRESHOLD))
        
        search_type = self._determine_citation_search_type(citation_type)
        
        service = CitationSearchServiceFactory.get_service(citation_type)
        
        context = SearchContextFactory.get_context(service, search_type)
        
        queryset = context.search(value, queryset, similarity_threshold=similarity_threshold)
        
        return queryset
    
    def _determine_search_type(self, representation_type):
        search_map = {
            'smiles': 'similarity',
            'api_id': 'exact',
            'inchi': 'exact',
            'inchi_key': 'exact',
            'formula': 'exact',
            'smarts': 'substructure',
            'fulltext': 'similarity'
        }
        
        return search_map.get(representation_type, 'exact')
    
    def _determine_citation_search_type(self, citation_type):
        search_map = {
            'doi': 'exact',
            'title': 'similarity'
        }

        return search_map.get(citation_type, 'exact')
    
    def filter_by_title(self, queryset, name, value):
        if self.request and hasattr(self.request, 'query_params'):
            params = self.request.query_params
        else:
            params = self.data
        
        search_type = params.get('search_type', 'similarity')
        
        threshold = float(params.get('similarity_threshold', FULLTEXT_SIMILARITY_SEARCH_THRESHOLD))
        
        try:
            service = LiteratureTitleSearchService
            context = SearchContextFactory.get_context(service, search_type)
            
            queryset = context.search(value, queryset, similarity_threshold=threshold)
            
            return queryset
        except ValueError as e:
            return queryset.none()