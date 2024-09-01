import re
from contextlib import redirect_stderr
from io import StringIO
from rdkit import Chem, rdBase
from rdkit.Chem import AllChem
from chempy import Substance
from random import choices
from string import digits
from django.core.exceptions import ValidationError

class RepresentationDetector:
    @staticmethod
    def detect_type(value):
        if RepresentationDetector._is_valid_smiles(value):
            return 'smiles'
        elif RepresentationDetector._is_valid_api_id(value):
            return 'api_id'
        elif RepresentationDetector._is_valid_inchi(value):
            return 'inchi'
        elif RepresentationDetector._is_valid_inchikey(value):
            return 'inchi_key'
        elif RepresentationDetector._is_valid_smarts(value):
            return 'smarts'
        elif RepresentationDetector._is_valid_chemical_formula(value):
            return 'formula'
        else:
            return 'fulltext'
    
    @staticmethod
    def _contains_atomic_number(smiles):
        atomic_number_pattern = r'\[#\d+\]'

        if re.search(atomic_number_pattern, smiles):
            return True
        
        return False

    @staticmethod
    def _rdkit_mol_from_smiles_can_generate_confs(rdkit_mol) -> bool:
        try:
            rdBase.LogToPythonStderr()

            rdkit_mol = Chem.AddHs(rdkit_mol)

            with StringIO() as buf:
                with redirect_stderr(buf):
                    AllChem.EmbedMolecule(rdkit_mol)
                    error_str_log = buf.getvalue()

            num_confomartions = rdkit_mol.GetNumConformers()

            return True if num_confomartions > 0 and not error_str_log else False
        except:
            return False

    @staticmethod
    def _is_valid_smiles(smiles: str) -> bool:
        mol = Chem.MolFromSmiles(smiles)

        if RepresentationDetector._contains_atomic_number(smiles):
            return False

        if mol == None:
            return False

        if not RepresentationDetector._rdkit_mol_from_smiles_can_generate_confs(mol):
            return False

        return True

    @staticmethod
    def _is_valid_inchi(query: str):
        return True if Chem.inchi.MolFromInchi(query, sanitize=True) else False

    @staticmethod
    def _is_valid_inchikey(query: str):
        return True if re.match(r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$', query) is not None else False

    @staticmethod
    def _is_valid_chemical_formula(query: str):
        try:
            substance = Substance.from_formula(query)
            return True
        except Exception:
            return False

    @staticmethod
    def _is_valid_smarts(query: str):
        mol = Chem.MolFromSmarts(query)

        if mol == None:
            return False

        return True

    @staticmethod
    def _is_valid_api_id(query: str):
        return True if re.match(r'^LSOA[0-9]{10}$', query) else False

class CitationDetector:
    @staticmethod
    def detect_type(value):
        if CitationDetector._is_valid_doi(value):
            return 'doi'
        else:
            return 'title'
    
    @staticmethod
    def _is_valid_doi(query: str):
        REGEX_DOI = re.compile(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/(?:(?![\"\&\'])\S)+)\b', flags = re.IGNORECASE | re.MULTILINE)
        
        return True if REGEX_DOI.match(query) is not None else False

def generate_random_sequence(length=10):
    return ''.join(choices(digits, k=length))

def validate_hex_color(value):
    HEXADECIMAL_COLOR_REGEX = re.compile(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', flags=re.IGNORECASE)
    
    if not HEXADECIMAL_COLOR_REGEX.fullmatch(value):
        raise ValidationError('{} is not a hexadecimal color'.format(value))