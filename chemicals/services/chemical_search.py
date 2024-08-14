from abc import ABC, abstractmethod
from django.db.models import Q, F
from django.db.models.functions import Greatest
from django.db.models.manager import BaseManager
from django.contrib.postgres.search import TrigramSimilarity
from .bingo_search import BingoSimilaritySearch, BingoSearch
from chemicals.models import Chemical


class ChemicalExactSearch(ABC):
    @staticmethod
    @abstractmethod
    def exact_search(query: str, queryset: BaseManager[Chemical], **parameters: dict) -> BaseManager[Chemical]:
        pass

class ChemicalSimilaritySearch(ABC):
    @staticmethod
    @abstractmethod
    def similarity_search(query: str, queryset: BaseManager[Chemical], similarity_thereshold: float) -> BaseManager[Chemical]:
        pass

class ChemicalSubstructureSearch(ABC):
    @staticmethod
    @abstractmethod
    def substructure_search(query: str, queryset: BaseManager[Chemical], **parameters: dict) -> BaseManager[Chemical]:
        pass

class ChemicalInchiSearch(ChemicalExactSearch):
    def exact_search(query, queryset, **parameters):
        return queryset.filter(identifiers__inchi=query)
    
class ChemicalInchiKeySearch(ChemicalExactSearch):
    def exact_search(query, queryset, **parameters):
        return queryset.filter(identifiers__inchi_key=query)
        
class ChemicalIUPACNameSearch(ChemicalExactSearch, ChemicalSimilaritySearch):
    def exact_search(query, queryset, **parameters):
        return queryset.filter(identifiers__iupac_name=query)
    
    def similarity_search(query, queryset, similarity_thereshold):
        return queryset.select_related('identifiers').annotate(
            iupac_similarity = TrigramSimilarity('identifiers__iupac_name', query)
        ).filter(
            iupac_similarity__gt=similarity_thereshold
        ).order_by(
            '-iupac_similarity'
        )

class ChemicalSynonymSearch(ChemicalExactSearch, ChemicalSimilaritySearch):
    def exact_search(query, queryset, **parameters):
        return queryset.filter(synonyms__name=query)
    
    def similarity_search(query, queryset, similarity_thereshold):
        return queryset.annotate(
            synonym_similarity = TrigramSimilarity('synonyms__name', query)
        ).filter(
            synonym_similarity__gt=similarity_thereshold
        ).order_by(
            '-synonym_similarity'
        ).prefetch_related('synonyms')

class ChemicalFullTextSearch(ChemicalSimilaritySearch):
    def similarity_search(query, queryset, similarity_thereshold):
        return queryset.select_related('identifiers').annotate(
            fulltext_similarity = Greatest(
                TrigramSimilarity('identifiers__iupac_name', query),
                TrigramSimilarity('synonyms__name', query)
            )
        ).filter(
            Q(fulltext_similarity__gt=similarity_thereshold)
        ).order_by(
            '-fulltext_similarity'
        ).prefetch_related('synonyms')

class ChemicalSMILESSearch(ChemicalExactSearch, ChemicalSimilaritySearch, ChemicalSubstructureSearch):
    @staticmethod
    def __add_parameters_as_str_seq(parameters: dict):
        parameters_str_seq = ''
        
        for parameter in parameters.keys():
            if parameter == 'TAU':
                parameters_str_seq += 'TAU'
                pass
            
        return parameters_str_seq
    
    def substructure_search(query, queryset, **parameters):
        parameters_str_seq = ChemicalSMILESSearch.__add_parameters_as_str_seq(parameters)
        
        return queryset.select_related('identifiers').annotate(
            bingo_sub = BingoSearch(F('identifiers__smiles'), 'bingo.sub',query, parameters_str_seq)
        ).filter(
            Q(bingo_sub=True)
        ).order_by(
            '-bingo_sub'
        )
    
    def exact_search(query, queryset, **parameters):
        parameters_str_seq = ChemicalSMILESSearch.__add_parameters_as_str_seq(parameters)

        return queryset.select_related('identifiers').annotate(
            bingo_exact = BingoSearch(F('identifiers__smiles'), 'bingo.exact', query, parameters_str_seq)
        ).filter(
            Q(bingo_exact=True)
        ).order_by(
            '-bingo_exact'
        )
    
    def similarity_search(query, queryset, similarity_thereshold):
        SIMILARITY_METRIC = 'Tanimoto'
        SIMILARITY_THERESHOLD_TOP = 1.0
        
        return queryset.select_related('identifiers').annotate(
            bingo_similarity=BingoSimilaritySearch(F('identifiers__smiles'), similarity_thereshold, SIMILARITY_THERESHOLD_TOP, query, SIMILARITY_METRIC)
        ).filter(
            Q(bingo_similarity=True)
        ).order_by(
            '-bingo_similarity'
        )

class ChemicalFormulaSearch(ChemicalExactSearch):
    @staticmethod
    def __separate_chemical_formula(formula: str):
        # Initialize an empty list to store parts of the separated formula
        result = []
        
        # Variable to keep track of the current element and its count
        element = ''

        for char in formula:
            if char.isupper():
                # If an uppercase letter is found, it signifies the start of a new element
                if element:
                    result.append(element)
                element = char  # Start a new element with the current uppercase letter
            else:
                element += char  # Append the lowercase letter or number to the current element

        # Add the last element to the result
        if element:
            result.append(element)

        # Join the result with spaces and return the formatted string
        return ' '.join(result)
    
    def exact_search(query, queryset, **parameters):
        separated_formula = ChemicalFormulaSearch.__separate_chemical_formula(query)
        
        formula_query = '= {}'.format(separated_formula)
        
        return queryset.select_related('identifiers').annotate(
            bingo_gross_formula = BingoSearch(F('identifiers__smiles'), 'bingo.gross', formula_query, '')
        ).filter(
            Q(bingo_gross_formula=True)
        ).order_by(
            '-bingo_gross_formula'
        )

class ChemicalSMARTSSearch(ChemicalSubstructureSearch):
    def substructure_search(query, queryset, **parameters):
        return queryset.select_related('identifiers').annotate(
            bingo_smarts = BingoSearch(F('identifiers__smiles'), 'bingo.smarts', query, '')
        ).filter(
            Q(bingo_smarts=True)
        ).order_by(
            '-bingo_smarts'
        )