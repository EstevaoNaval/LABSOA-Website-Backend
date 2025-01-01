import re
from django.db import models
from django.utils.text import slugify
import hashlib
import base64
import time
import os

from user.models import User

from .util.util import generate_random_sequence, validate_hex_color

class BaseModel(models.Model):
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class HashAPIIdBaseModel(BaseModel):
    api_id = models.CharField(max_length=14, unique=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.api_id:
            self.api_id = self.__generate_unique_api_id()
        
        super().save(*args, **kwargs)
    
    def __generate_unique_api_id(self, length: int = 10):
        current_time = str(time.time()).encode('utf-8')
        random_bytes = os.urandom(16)
        combined = current_time + random_bytes
        hash_object = hashlib.sha256(combined)
        unique_id = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')[:length]

        while Chemical.objects.filter(api_id=unique_id).exists():
            current_time = str(time.time()).encode('utf-8')
            random_bytes = os.urandom(16)
            combined = current_time + random_bytes
            hash_object = hashlib.sha256(combined)
            unique_id = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')[:length]
        
        return unique_id

class Literature(HashAPIIdBaseModel):
    doi = models.CharField(unique=True)
    title = models.TextField()
    publication_date = models.DateField()
    publication_name = models.TextField()

class Chemical(BaseModel):
    chem_depiction_image = models.ImageField(upload_to='depictions/', null=True)
    literature = models.ManyToManyField(to=Literature, related_name='chemicals')
    api_id = models.CharField(max_length=14, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='chemicals')
    
    def save(self, *args, **kwargs):
        if not self.api_id:
            self.api_id = self.__generate_unique_api_id()
        
        super().save(*args, **kwargs)
    
    def __generate_unique_api_id(self, length: int = 10):
        prefix = "LSOA"
        while True:
            suffix = generate_random_sequence(length)
            api_id = f"{prefix}{suffix}"
            
            if not Chemical.objects.filter(api_id=api_id).exists():
                return api_id

class Identifier(HashAPIIdBaseModel):
    iupac_name = models.TextField()
    chem_formula = models.TextField()
    inchi = models.TextField()
    inchi_key = models.TextField()
    smiles = models.TextField()
    slug = models.TextField(null=True, blank=True)
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='identifiers')
    
    def __clean_iupac_name(self, iupac_name):
        cleaned_name = re.sub(r'[^_\d\w\s-]', '', iupac_name)
        cleaned_name = re.sub(r'[-\s]+', '-', cleaned_name)
        return cleaned_name.lower()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.__clean_iupac_name(self.iupac_name))
            random_sequence = generate_random_sequence(8)
            self.slug = f"{base_slug}-{random_sequence}"
        
        super().save(*args, **kwargs)
    
class PhysicalProperty(HashAPIIdBaseModel):
    molecular_weight = models.FloatField()
    volume = models.FloatField()
    count_atom = models.PositiveSmallIntegerField()
    count_heteroatom = models.PositiveSmallIntegerField()
    count_heavy_atom = models.PositiveSmallIntegerField()
    count_aromatic_heavy_atom = models.PositiveSmallIntegerField()
    count_rotatable_bond = models.PositiveSmallIntegerField()
    count_h_bond_acceptor = models.PositiveSmallIntegerField()
    count_h_bond_donor = models.PositiveSmallIntegerField()
    count_ring = models.PositiveSmallIntegerField()
    count_carbon = models.PositiveSmallIntegerField()
    mp_lower_bound = models.FloatField(null=True)
    mp_upper_bound = models.FloatField(null=True)
    state_of_matter = models.CharField(blank=True)
    color = models.CharField(blank=True)
    color_hexadecimal = models.CharField(validators=[validate_hex_color], blank=True)
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='physical_properties')

class PhysicochemicalProperty(HashAPIIdBaseModel):
    fraction_csp3 = models.FloatField()
    molar_refractivity = models.FloatField()
    tpsa = models.FloatField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='physicochemical_properties')

class PartitionCoefficient(HashAPIIdBaseModel):
    wildman_crippen_logp = models.FloatField()
    xlogp = models.FloatField()
    jplogp = models.FloatField()
    mouriguchi_logp = models.FloatField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='partition_coefficients')

class Solubility(HashAPIIdBaseModel):
    esol_logs = models.FloatField()
    filter_it_logs = models.FloatField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='solubilities')
    
class QsarScore(HashAPIIdBaseModel):
    qed_score = models.FloatField()
    synthetic_accessibility_score = models.FloatField()
    natural_product_score = models.FloatField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE,related_name='qsar_scores')

class DrugLikeRule(HashAPIIdBaseModel):
    count_lipinski_violation = models.PositiveSmallIntegerField()
    count_ghose_violation = models.PositiveSmallIntegerField()
    count_veber_violation = models.PositiveSmallIntegerField()
    count_egan_violation = models.PositiveSmallIntegerField()
    count_muegge_violation = models.PositiveSmallIntegerField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='druglike_rules')

class Pharmacokinetics(HashAPIIdBaseModel):
    gastrointestinal_absorption = models.BooleanField()
    blood_brain_barrier_permeation = models.BooleanField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='pharmacokinetics')
    
class P450Inhibition(HashAPIIdBaseModel):
    cyp1a2_inhibitor = models.BooleanField()
    cyp2c9_inhibitor = models.BooleanField()
    cyp2c19_inhibitor = models.BooleanField()
    cyp2d6_inhibitor = models.BooleanField()
    cyp3a4_inhibitor = models.BooleanField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='p450_inhibitors')

class UndesirableSubstructureAlert(HashAPIIdBaseModel):
    count_pains_alert = models.PositiveSmallIntegerField()
    count_brenk_alert = models.PositiveSmallIntegerField()
    chemical = models.OneToOneField(to=Chemical, on_delete=models.CASCADE, related_name='undesirable_substructure_alerts')

class Synonym(HashAPIIdBaseModel):
    name = models.TextField()
    chemical = models.ForeignKey(to=Chemical, on_delete=models.CASCADE, related_name='synonyms')

class Conformation(HashAPIIdBaseModel):
    conf_file = models.FileField(upload_to='confs/')
    chemical = models.ForeignKey(to=Chemical, on_delete=models.CASCADE, related_name='conformations')


    
    