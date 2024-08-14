from rest_framework import serializers
from .models import *

class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        exclude=['id','created_at','update_at']

class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        exclude=['id','created_at','update_at', 'chemical']

class PhysicalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProperty
        exclude=['id','created_at','update_at', 'chemical']
        
class PhysicochemicalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicochemicalProperty
        exclude=['id','created_at','update_at', 'chemical']
        
class PartitionCoefficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartitionCoefficient
        exclude=['id','created_at','update_at', 'chemical']
        
class SolubilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Solubility
        exclude=['id','created_at','update_at', 'chemical']
        
class QsarScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QsarScore
        exclude=['id','created_at','update_at', 'chemical']

class DrugLikeRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugLikeRule
        exclude=['id','created_at','update_at', 'chemical']
        
class PharmacokineticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacokinetics
        exclude=['id','created_at','update_at', 'chemical']
        
class P450InhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = P450Inhibition
        exclude=['id','created_at','update_at', 'chemical']

class UndesirableSubstructureAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndesirableSubstructureAlert
        exclude=['id','created_at','update_at', 'chemical']
        
class ToxicityPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToxicityPrediction
        exclude=['id','created_at','update_at', 'chemical']

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        exclude=['id','created_at','update_at', 'chemical']
        
class ConformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conformation
        exclude=['id','created_at','update_at', 'chemical']
        
class ChemicalSerializer(serializers.ModelSerializer):
    identifier = IdentifierSerializer(source='identifiers')
    literature = LiteratureSerializer()
    physical_property = PhysicalPropertySerializer(source='physical_properties')
    physicochemical_property = PhysicochemicalPropertySerializer(source='physicochemical_properties')
    partition_coefficient = PartitionCoefficientSerializer(source='partition_coefficients')
    solubility = SolubilitySerializer(source='solubilities')
    qsar_score = QsarScoreSerializer(source='qsar_scores')
    druglike_rule = DrugLikeRuleSerializer(source='druglike_rules')
    pharmacokinetics = PharmacokineticsSerializer()
    p450_inhibition = P450InhibitionSerializer(source='p450_inhibitors')
    undesirable_substructure_alert = UndesirableSubstructureAlertSerializer(source='undesirable_substructure_alerts')
    toxicity_prediction = ToxicityPredictionSerializer(source='toxicity_predictions')
    synonym = SynonymSerializer(many=True, required=False, source='synonyms')
    conformation = ConformationSerializer(many=True, source='conformations')
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    class Meta:
        model = Chemical
        fields = ['api_id', 
                  'chem_depiction_image', 
                  'literature', 
                  'identifier',
                  'physical_property',
                  'physicochemical_property',
                  'partition_coefficient',
                  'solubility',
                  'qsar_score',
                  'druglike_rule',
                  'pharmacokinetics',
                  'p450_inhibition',
                  'undesirable_substructure_alert',
                  'toxicity_prediction',
                  'synonym',
                  'conformation']

class ChemicalAutocompleteSerializer(serializers.ModelSerializer):
    identifier = IdentifierSerializer(read_only=True, source='identifiers')
    synonym = SynonymSerializer(read_only=True, many=True, source='synonyms')
     
    class Meta:
        model = Chemical
        fields = ['api_id', 'identifier', 'synonym']