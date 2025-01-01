import uuid

from django.db import IntegrityError

from rest_framework import serializers

from .models import *
from .util.util import ManuscriptMetadata

class LiteratureSerializer(serializers.ModelSerializer):
    doi = serializers.CharField(validators=[])
    
    class Meta:
        model = Literature
        exclude=['id','created_at','update_at']
        read_only_fields=['api_id','title','publication_date','publication_name']

class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']

class PhysicalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProperty
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class PhysicochemicalPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicochemicalProperty
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class PartitionCoefficientSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartitionCoefficient
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class SolubilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Solubility
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class QsarScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = QsarScore
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']

class DrugLikeRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugLikeRule
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class PharmacokineticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacokinetics
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class P450InhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = P450Inhibition
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']

class UndesirableSubstructureAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndesirableSubstructureAlert
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class ConformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conformation
        exclude=['id','created_at','update_at', 'chemical']
        read_only_fields=['api_id']
        
class ChemicalSerializer(serializers.ModelSerializer):
    api_id = serializers.CharField(required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    literature = LiteratureSerializer(required=False, many=True)
    identifier = IdentifierSerializer(source='identifiers', required=False)
    physical_property = PhysicalPropertySerializer(source='physical_properties', required=False)
    physicochemical_property = PhysicochemicalPropertySerializer(source='physicochemical_properties', required=False)
    partition_coefficient = PartitionCoefficientSerializer(source='partition_coefficients', required=False)
    solubility = SolubilitySerializer(source='solubilities', required=False)
    qsar_score = QsarScoreSerializer(source='qsar_scores', required=False)
    druglike_rule = DrugLikeRuleSerializer(source='druglike_rules', required=False)
    pharmacokinetics = PharmacokineticsSerializer(required=False)
    p450_inhibition = P450InhibitionSerializer(source='p450_inhibitors', required=False)
    undesirable_substructure_alert = UndesirableSubstructureAlertSerializer(source='undesirable_substructure_alerts', required=False)
    synonym = SynonymSerializer(many=True, required=False, source='synonyms')
    conformation = ConformationSerializer(many=True, required=False, source='conformations')
    
    def create(self, validated_data):
        # Pop fields related to nested serializers
        nested_fields = [
            'literature', 'identifiers', 'physical_properties',
            'physicochemical_properties', 'partition_coefficients', 'solubilities',
            'qsar_scores', 'druglike_rules', 'pharmacokinetics', 'p450_inhibitors',
            'undesirable_substructure_alerts', 'synonyms', 'conformations'
        ]
        
        # Extract nested data
        nested_data = {field: validated_data.pop(field, []) for field in nested_fields}

        # Create the main instance
        chemical = Chemical.objects.create(**validated_data)

        # Handle nested data creation
        if nested_data['literature']:
            for lit in nested_data['literature']:
                doi = lit.get('doi', None)
                if not doi:
                    continue  # Skip entries without a DOI
                
                try:
                    # Fetch metadata for the manuscript
                    manuscript_metadata = ManuscriptMetadata(doi)
    
                    # Attempt to get or create the literature record
                    literature, _ = Literature.objects.get_or_create(
                        doi=manuscript_metadata.get___doi(),
                        defaults={
                            'title': manuscript_metadata.get___title(),
                            'publication_date': manuscript_metadata.get___publication_date(),
                            'publication_name': manuscript_metadata.get___publication_name()
                        }
                    )
                except IntegrityError:
                    # Handle potential race condition or duplicate DOI
                    literature = Literature.objects.get(doi=manuscript_metadata.get___doi())
                except Exception as e:
                    # Log or handle unexpected errors
                    print(f"Error processing DOI {doi}: {str(e)}")
                    continue
                
                # Add literature to the chemical instance
                chemical.literature.add(literature)
        
        if nested_data['identifiers']:
            Identifier.objects.create(**nested_data['identifiers'], chemical=chemical)
        
        if nested_data['physical_properties']:
            PhysicalProperty.objects.create(**nested_data['physical_properties'], chemical=chemical)
        
        if nested_data['physicochemical_properties']:
            PhysicochemicalProperty.objects.create(**nested_data['physicochemical_properties'], chemical=chemical)
        
        if nested_data['partition_coefficients']:
            PartitionCoefficient.objects.create(**nested_data['partition_coefficients'], chemical=chemical)
        
        if nested_data['solubilities']:
            Solubility.objects.create(**nested_data['solubilities'], chemical=chemical)
        
        if nested_data['qsar_scores']:
            QsarScore.objects.create(**nested_data['qsar_scores'], chemical=chemical)
        
        if nested_data['druglike_rules']:
            DrugLikeRule.objects.create(**nested_data['druglike_rules'], chemical=chemical)
        
        if nested_data['pharmacokinetics']:
            Pharmacokinetics.objects.create(**nested_data['pharmacokinetics'], chemical=chemical)
        
        if nested_data['p450_inhibitors']:
            P450Inhibition.objects.create(**nested_data['p450_inhibitors'], chemical=chemical)
        
        if nested_data['undesirable_substructure_alerts']:
            UndesirableSubstructureAlert.objects.create(**nested_data['undesirable_substructure_alerts'], chemical=chemical)
        
        if nested_data['synonyms']:
            for synonym_data in nested_data['synonyms']:
                Synonym.objects.create(**synonym_data, chemical=chemical)
        
        if nested_data['conformations']:
            for conf in nested_data['conformations']:
                conf['conf_file'].name = f"conf_{uuid.uuid4().hex}.sdf"
                Conformation.objects.create(chemical=chemical, conf_file=conf['conf_file'])

        return chemical
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        
        validated_data.pop('api_id', None)
        
        literature_data = validated_data.pop('literature', None)
        if literature_data is not None:
            literature_api_id = instance.literature.api_id
            
            Literature.objects.update_or_create(
                api_id=literature_api_id,
                defaults=literature_data
            )
        
        identifier_data = validated_data.pop('identifiers', None)
        if identifier_data is not None:
            identifier_api_id = instance.identifiers.api_id
            
            Identifier.objects.update_or_create(
                api_id=identifier_api_id, 
                chemical=instance, 
                defaults=identifier_data
            )
        
        physical_property_data = validated_data.pop('physical_properties', None)
        if physical_property_data is not None:
            physical_property_api_id = instance.physical_properties.api_id
            
            PhysicalProperty.objects.update_or_create(
                api_id = physical_property_api_id,
                chemical=instance,
                defaults=physical_property_data
            )
        
        physicochemical_property_data = validated_data.pop('physicochemical_properties', None)
        if physicochemical_property_data is not None:
            physicochemical_property_api_id = instance.physicochemical_properties.api_id
            
            PhysicochemicalProperty.objects.update_or_create(
                api_id = physicochemical_property_api_id,
                chemical=instance,
                defaults=physicochemical_property_data
            )
        
        partition_coefficient_data = validated_data.pop('partition_coefficients', None)
        if partition_coefficient_data is not None:
            partition_coefficient_api_id = instance.partition_coefficients.api_id
            
            PartitionCoefficient.objects.update_or_create(
                api_id = partition_coefficient_api_id,
                chemical = instance,
                defaults=partition_coefficient_data
            )
            
        solubility_data = validated_data.pop('solubilities', None)
        if solubility_data is not None:
            solubility_api_id = instance.solubilities.api_id
            
            Solubility.objects.update_or_create(
                api_id = solubility_api_id,
                chemical = instance,
                defaults= solubility_data
            )
        
        qsar_score_data = validated_data.pop('qsar_scores', None)
        if qsar_score_data is not None:
            qsar_score_api_id = instance.qsar_scores.api_id
            
            QsarScore.objects.update_or_create(
                api_id = qsar_score_api_id,
                chemical = instance,
                defaults = qsar_score_data
            )
            
        druglike_rule_data = validated_data.pop('druglike_rules', None)
        if druglike_rule_data is not None:
            druglike_rule_api_id = instance.druglike_rules.api_id
            
            DrugLikeRule.objects.update_or_create(
                api_id = druglike_rule_api_id,
                chemical = instance,
                defaults = druglike_rule_data
            )
        
        pharmacokinetics_data = validated_data.pop('pharmacokinetics', None)
        if pharmacokinetics_data is not None:
            pharmacokinetics_api_id = instance.pharmacokinetics.api_id
            
            Pharmacokinetics.objects.update_or_create(
                api_id = pharmacokinetics_api_id,
                chemical = instance,
                defaults = pharmacokinetics_data
            )
        
        p450_inhibition_data = validated_data.pop('p450_inhibitors', None)
        if p450_inhibition_data is not None:
            p450_inhibition_api_id = instance.p450_inhibitors.api_id
            
            P450Inhibition.objects.update_or_create(
                api_id = p450_inhibition_api_id,
                chemical = instance,
                defaults = p450_inhibition_data
            )
        
        undesirable_substructure_alert_data = validated_data.pop('undesirable_substructure_alerts', None)
        if undesirable_substructure_alert_data is not None:
            undesirable_substructure_alert_api_id = instance.undesirable_substructure_alerts.api_id
            
            UndesirableSubstructureAlert.objects.update_or_create(
                api_id = undesirable_substructure_alert_api_id,
                chemical = instance,
                defaults = undesirable_substructure_alert_data
            )
        
        synonyms_data = validated_data.pop('synonyms', None)
        if synonyms_data:
            for synonym_data in synonyms_data:
                synonym_api_id = synonym_data.get('api_id')
                
                Synonym.objects.update_or_create(
                    api_id = synonym_api_id,
                    chemical = instance,
                    defaults = synonym_data
                )
        
        if request and hasattr(request, 'FILES'):
            conformations_files = request.FILES
            
            for key, files in conformations_files.lists():
                if key.startswith("conformations") and "conf_file" in key:
                    for conf in files:
                        conf.name = f'conf_{uuid.uuid4().hex}.sdf'
                        Conformation.objects.update_or_create(
                            chemical=instance,
                            conf_file=conf
                        )
                        
                if 'depiction_image' in key:
                    chem_depiction_image = files[0]
                    chem_depiction_image.name = f'depiction_{uuid.uuid4().hex}.svg'
                    instance.chem_depiction_image = chem_depiction_image
        
        instance.save()
        
        return instance
    
    class Meta:
        model = Chemical
        fields = [
            'api_id',
            'user',
            'created_at', 
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
            'synonym',
            'conformation',
        ]
        read_only_fields=['api_id']

class IdentifierAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = ['iupac_name', 'smiles']

class ChemicalAutocompleteSerializer(serializers.ModelSerializer):
    identifier = IdentifierAutocompleteSerializer(read_only=True, source='identifiers')
    synonym = SynonymSerializer(read_only=True, many=True, source='synonyms')
     
    class Meta:
        model = Chemical
        fields = ['api_id', 'identifier', 'synonym']

class IdentifierSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = ['iupac_name', 'chem_formula']

class PhysicalPropertySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProperty
        fields = ['molecular_weight', 'state_of_matter', 'mp_lower_bound', 'mp_upper_bound']

class ChemicalSummarySerializer(serializers.ModelSerializer):
    identifier = IdentifierSummarySerializer(read_only=True, source='identifiers')
    physical_property = PhysicalPropertySummarySerializer(read_only=True, source='physical_properties')
    
    class Meta:
        model = Chemical
        fields = ['api_id', 'chem_depiction_image', 'identifier', 'physical_property']
        
class PhysicalPropertyPropListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProperty
        fields = [
            'molecular_weight', 
            'count_rotatable_bond', 
            'count_heavy_atom', 
            'count_h_bond_donor',
            'count_h_bond_acceptor',
            'mp_lower_bound',
            'mp_upper_bound',
        ]

class PhysicochemicalPropertyPropListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicochemicalProperty
        fields = ['tpsa']

class PartitionCoefficientPropListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartitionCoefficient
        fields = ['jplogp']

class UndesirableSubstructureAlertPropListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UndesirableSubstructureAlert
        fields = ['count_pains_alert']

class DrugLikeRulePropListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugLikeRule
        fields = ['count_lipinski_violation']

class ChemicalPropListSerializer(serializers.ModelSerializer):
    physical_property = PhysicalPropertyPropListSerializer(read_only=True, source='physical_properties')
    physicochemical_property = PhysicochemicalPropertyPropListSerializer(read_only=True, source='physicochemical_properties')
    partition_coefficient = PartitionCoefficientPropListSerializer(read_only=True, source='partition_coefficients')
    undesirable_substructure_alert = UndesirableSubstructureAlertPropListSerializer(read_only=True, source='undesirable_substructure_alerts')
    druglike_rule = DrugLikeRulePropListSerializer(read_only=True, source='druglike_rules')
    
    class Meta:
        model = Chemical
        fields = [
            'api_id', 
            'physical_property', 
            'physicochemical_property', 
            'partition_coefficient', 
            'undesirable_substructure_alert',
            'druglike_rule'
        ]