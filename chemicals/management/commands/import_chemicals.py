# chemicals/management/commands/import_chemicals.py
import csv
import logging
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db import transaction
from user.models import User
from chemicals.models import *
from .utils import find_files, is_numeric, ManuscriptMetadata

class Command(BaseCommand):
    help = 'Import chemicals from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported')
        parser.add_argument("--base-path", type=str, required=True, help='The base path for the chemicals conformations')
        parser.add_argument("--user-email", type=str, required=True, help='Registered user email')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        chem_confs_base_path = options['base_path']
        user_email = options['user-email']
        logger = logging.getLogger('django')
        
        CHEMICAL_CONFS_FILE_FORMAT = 'sdf'
        
        CHEMICAL_DEPICTION_IMAGE_FILE_FORMAT = 'svg'
        
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                with transaction.atomic():
                    for row in reader:
                        
                        literature = None
                        if row.get('doi'):
                            manuscript_metadata = ManuscriptMetadata(row.get('doi'))
                            literature, created = Literature.objects.update_or_create(
                                doi = manuscript_metadata.get___doi(),
                                defaults={
                                    'title': manuscript_metadata.get___title(),
                                    'publication_date': manuscript_metadata.get___publication_date(),
                                    'publication_name': manuscript_metadata.get___publication_name()
                                }
                            )
                        
                        user = User.objects.get(email=user_email)
                        
                        chemical_depiction_image_base_file_path = os.path.join(chem_confs_base_path, row.get('id'))
                        depiction_files = find_files(chemical_depiction_image_base_file_path, CHEMICAL_DEPICTION_IMAGE_FILE_FORMAT)
                        for depiction_file_path in depiction_files:
                            depiction_filename = os.path.basename(depiction_file_path)
                            with open(depiction_file_path, 'r') as depiction_file:
                                chemical = Chemical.objects.create(chem_depiction_image=File(depiction_file, name=depiction_filename), user=user)
                                if literature:
                                    chemical.literature.set([literature])
                        
                        Identifier.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'iupac_name': row.get('iupac'),
                                'chem_formula': row.get('formula'),
                                'inchi': row.get('inchi'),
                                'inchi_key': row.get('inchi_key'),
                                'smiles': row.get('smiles'),
                            }
                        )
                        
                        PhysicalProperty.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'molecular_weight': row.get('mass_weight'),
                                'volume': row.get('volume'),
                                'count_atom': row.get('num_atom'),
                                'count_heteroatom': row.get('num_heteroatom'),
                                'count_heavy_atom': row.get('num_heavy_atom'),
                                'count_aromatic_heavy_atom': row.get('num_arom_heavy_atom'),
                                'count_rotatable_bond': row.get('num_rotatable_bond'),
                                'count_h_bond_acceptor': row.get('num_h_bond_accept'),
                                'count_h_bond_donor': row.get('num_h_bond_donor'),
                                'count_ring': row.get('num_ring'),
                                'count_carbon': row.get('num_carbon'),
                                'mp_lower_bound': row.get('melting_point_lower_bound') if is_numeric(row.get('melting_point_lower_bound')) else None,
                                'mp_upper_bound': row.get('melting_point_upper_bound') if is_numeric(row.get('melting_point_upper_bound')) else None,
                                'state_of_matter': row.get('state_of_matter'),
                                'color': row.get('color'),
                                'color_hexadecimal': row.get('color_hex_value')
                            }
                        )
                        
                        PhysicochemicalProperty.objects.update_or_create(
                            chemical=chemical,
                            defaults= {
                                'fraction_csp3': row.get('fraction_csp3'),
                                'molar_refractivity': row.get('molar_refractivity'),
                                'tpsa': row.get('tpsa')
                            }
                        )
                        
                        PartitionCoefficient.objects.update_or_create(
                            chemical=chemical,
                            defaults= {
                                'wildman_crippen_logp': row.get('wlogp'),
                                'xlogp': row.get('xlogp2'),
                                'jplogp': row.get('jplogp'),
                                'mouriguchi_logp': row.get('mlogp')
                            }
                        )
                        
                        Solubility.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'esol_logs': row.get('esol_logs'),
                                'filter_it_logs': row.get('filter_it_logs')
                            }
                        )
                        
                        QsarScore.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'qed_score': row.get('qed_score'),
                                'synthetic_accessibility_score': row.get('synthetic_accessibility_score'),
                                'natural_product_score': row.get('natural_product_score')
                            }
                        )
                        
                        DrugLikeRule.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'count_lipinski_violation': row.get('num_lipinski_violation'),
                                'count_ghose_violation': row.get('num_ghose_violation'),
                                'count_veber_violation': row.get('num_veber_violation'),
                                'count_egan_violation': row.get('num_egan_violation'),
                                'count_muegge_violation': row.get('num_muegge_violation')
                            }
                        )
                        
                        Pharmacokinetics.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'gastrointestinal_absorption': int(row.get('gi_absorption')),
                                'blood_brain_barrier_permeation': int(row.get('bbb_permeant'))
                            }
                        )
                        
                        P450Inhibition.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'cyp1a2_inhibitor': int(row.get('cyp1a2_inhibitor')),
                                'cyp2c9_inhibitor': int(row.get('cyp2c9_inhibitor')),
                                'cyp2c19_inhibitor': int(row.get('cyp2c19_inhibitor')),
                                'cyp2d6_inhibitor': int(row.get('cyp2d6_inhibitor')),
                                'cyp3a4_inhibitor': int(row.get('cyp3a4_inhibitor'))
                            }
                        )
                        
                        UndesirableSubstructureAlert.objects.update_or_create(
                            chemical=chemical,
                            defaults={
                                'count_pains_alert': row.get('num_pains_violation'),
                                'count_brenk_alert': row.get('num_brenk_violation')
                            }
                        )
                        
                        chemical_confs_base_file_path = os.path.join(chem_confs_base_path, row.get('id'), CHEMICAL_CONFS_FILE_FORMAT)
                        conformation_files = find_files(chemical_confs_base_file_path, CHEMICAL_CONFS_FILE_FORMAT)
                        for conformation_file_path in conformation_files:
                            with open(conformation_file_path, 'rb') as conf_file:
                                conf_filename = os.path.basename(conformation_file_path)
                                conformation, conf_created = Conformation.objects.get_or_create(
                                    chemical=chemical,
                                    conf_file=conf_filename,
                                    defaults={'conf_file': File(conf_file, name=conf_filename)}
                                )
                                if not conf_created:
                                    # If the conformation already exists, update the file
                                    conformation.conf_file.save(conf_filename, File(conf_file, name=conf_filename), save=True)
                                    
                        logger.info(f'Created chemical {chemical.api_id}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported chemicals from "{csv_file}"'))
        except Exception as e:
            logger.error(f'Error importing chemicals: {e}')
            self.stderr.write(self.style.ERROR('Error importing chemicals'))
