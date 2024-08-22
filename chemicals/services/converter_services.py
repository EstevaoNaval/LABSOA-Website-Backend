from abc import ABC, abstractmethod
from rdkit.Chem import MolToSmiles, MolFromMolFile, MolFromInchi, SDMolSupplier

class ChemicalConverterToSmiles(ABC):
    @abstractmethod
    def to_smiles(self) -> str:
        pass
    
class ChemicalInchiConverterToSmiles(ChemicalConverterToSmiles):
    def __init__(self, inchi) -> None:
        self.inchi = inchi
    
    def to_smiles(self):
        mol = MolFromInchi(self.inchi)
        
        smiles = MolToSmiles(mol)
        
        return smiles
    
class ChemicalMolFileConverterToSmiles(ChemicalConverterToSmiles):
    def __init__(self, mol_file) -> None:
        self.mol_file = mol_file
        
    def to_smiles(self) -> str:
        smiles = ''
        
        mol = MolFromMolFile(self.mol_file)
        
        if mol is not None:
            smiles = MolToSmiles(mol)
            
        return smiles
    
class ChemicalSDFConverterToSmiles(ChemicalConverterToSmiles):
    def __init__(self, sdf_file) -> None:
        self.sdf_file = sdf_file
        
    def to_smiles(self) -> str:
        smiles = ''
        
        supplier = SDMolSupplier(self.sdf_file)
        
        for mol in supplier:
            if mol is not None:
                smiles = MolToSmiles(mol)
                
                return smiles
            
        return smiles