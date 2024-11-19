from django.db import migrations
from chemicals.models import Identifier

class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0004_iupac_fulltext_search_idx'),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS labsoa_smiles_bingo_idx on {} using bingo_idx (smiles bingo.molecule);".format(Identifier._meta.db_table),
            reverse_sql="DROP INDEX labsoa_smiles_bingo_idx;"
        ),
    ]
