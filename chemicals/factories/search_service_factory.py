from chemicals.services.search_services import (
    SmilesSearchService,
    APIIdSearchService,
    InchiSearchService,
    InchiKeySearchService,
    FormulaSearchService,
    SmartsSearchService,
    FullTextSearchService
)

class SearchServiceFactory:
    service_mapping = {
        'smiles': SmilesSearchService,
        'api_id': APIIdSearchService,
        'inchi': InchiSearchService,
        'inchi_key': InchiKeySearchService,
        'formula': FormulaSearchService,
        'smarts': SmartsSearchService,
        'fulltext': FullTextSearchService
    }

    @staticmethod
    def get_service(representation_type):
        service_class = SearchServiceFactory.service_mapping.get(representation_type)
        
        if service_class is None:
            raise ValueError(f"Type of chemical representation '{representation_type}' not supported.")
        
        return service_class
