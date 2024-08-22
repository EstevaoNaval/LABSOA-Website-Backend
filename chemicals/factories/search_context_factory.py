from chemicals.contexts.exact_search_context import ExactSearchContext
from chemicals.contexts.similarity_search_context import SimilaritySearchContext
from chemicals.contexts.substructure_search_context import SubstructureSearchContext

class SearchContextFactory:
    context_mapping = {
        'exact': ExactSearchContext,
        'similarity': SimilaritySearchContext,
        'substructure': SubstructureSearchContext,
    }

    @staticmethod
    def get_context(service, search_type):
        context_class = SearchContextFactory.context_mapping.get(search_type)
        if context_class is None:
            raise ValueError(f"Seach type '{search_type}' not supported.")
        
        if not hasattr(service, f'{search_type}_search'):
            raise ValueError(f"'{service.__class__.__name__}' service doesn't support '{search_type}' search type.")
        
        return context_class(service)
