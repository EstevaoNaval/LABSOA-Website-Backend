from django.db import migrations
from chemicals.models import Synonym

class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0005_labsoa_smiles_bingo_idx')
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS synonym_fulltext_search_idx ON {} USING GIN(name gin_trgm_ops);".format(Synonym._meta.db_table),
            reverse_sql="DROP INDEX synonym_fulltext_search_idx;"
        ),
    ]
