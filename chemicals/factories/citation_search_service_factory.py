from chemicals.services.search_services import (
    LiteratureDoiSearchService,
    LiteratureTitleSearchService
)

class CitationSearchServiceFactory:
    service_mapping = {
        'doi': LiteratureDoiSearchService,
        'title': LiteratureTitleSearchService
    }

    @staticmethod
    def get_service(citation_type):
        service_class = CitationSearchServiceFactory.service_mapping.get(citation_type)
        
        if service_class is None:
            raise ValueError(f"Type of citation '{citation_type}' not supported.")
        
        return service_class
