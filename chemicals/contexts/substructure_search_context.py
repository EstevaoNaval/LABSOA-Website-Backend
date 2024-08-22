from chemicals.services.search_services import SubstructureSearch

class SubstructureSearchContext:
    def __init__(self, substructure_search_service = None):
        self.__substructure_search_service = substructure_search_service
        
    def set_substructure_search_service(self, chem_substructure_search: SubstructureSearch):
        self.__substructure_search_service = chem_substructure_search
        
    def search(self, query, queryset, **parameters):
        if not self.__substructure_search_service:
            raise ValueError('A substructure search service must be set before substructure searching a chemical.')
        
        return self.__substructure_search_service.substructure_search(query, queryset, **parameters)