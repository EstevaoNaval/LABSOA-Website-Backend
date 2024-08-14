from .chemical_search import ChemicalExactSearch, ChemicalSimilaritySearch, ChemicalSubstructureSearch

class ChemicalExactSearchContext:
    def __init__(self):
        self.__chemical_exact_search = None
        
    def set_chemical_exact_search(self, chem_exact_search: ChemicalExactSearch):
        self.__chemical_exact_search = chem_exact_search
    
    def exact_search(self, query, queryset, **parameters):
        if not self.__chemical_exact_search:
            raise ValueError('A chemical exact search algorithm must be set before exact searching a chemical.')
        
        return self.__chemical_exact_search.exact_search(query, queryset, **parameters)

class ChemicalSimilaritySearchContext:
    def __init__(self):
        self.__chemical_similarity_search = None
        
    def set_chemical_similarity_search(self, chem_similarity_search: ChemicalSimilaritySearch):
        self.__chemical_similarity_search = chem_similarity_search
    
    def similarity_search(self, query, queryset, similarity_thereshold):
        if not self.__chemical_similarity_search:
            raise ValueError('A chemical similarity search algorithm must be set before similarity searching a chemical.')
        
        return self.__chemical_similarity_search.similarity_search(query, queryset, similarity_thereshold)
    
class ChemicalSubstructureSearchContext:
    def __init__(self):
        self.__chemical_substructure_search = None
        
    def set_chemical_substructure_search(self, chem_substructure_search: ChemicalSubstructureSearch):
        self.__chemical_substructure_search = chem_substructure_search
        
    def substructure_search(self, query, queryset, **parameters):
        if not self.__chemical_substructure_search:
            raise ValueError('A chemical substructure search algorithm must be set before substructure searching a chemical.')
        
        return self.__chemical_substructure_search.substructure_search(query, queryset, **parameters)