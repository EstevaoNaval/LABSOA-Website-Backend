from chemicals.services.search_services import SimilaritySearch

class SimilaritySearchContext:
    def __init__(self, similarity_search_service = None):
        self.__similarity_search_service = similarity_search_service
        
    def set_similarity_search_service(self, chem_similarity_search: SimilaritySearch):
        self.__similarity_search_service = chem_similarity_search
    
    def search(self, query, queryset, **parameters):
        if not self.__similarity_search_service:
            raise ValueError('A similarity search service must be set before similarity searching a chemical.')
        
        return self.__similarity_search_service.similarity_search(query, queryset, similarity_threshold=parameters['similarity_threshold'])