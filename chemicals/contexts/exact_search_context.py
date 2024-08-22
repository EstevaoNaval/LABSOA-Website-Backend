from chemicals.services.search_services import ExactSearch

class ExactSearchContext:
    def __init__(self, exact_search_service = None):
        self.__exact_search_service = exact_search_service
        
    def set_exact_search_service(self, chem_exact_search: ExactSearch):
        self.__exact_search_service = chem_exact_search
    
    def search(self, query, queryset, **parameters):
        if not self.__exact_search_service:
            raise ValueError('A exact search service must be set before exact searching a chemical.')
        
        return self.__exact_search_service.exact_search(query, queryset, **parameters)