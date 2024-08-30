from django.db import migrations
from chemicals.models import Literature

class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0005_labsoa_smiles_bingo_idx')
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS literature_title_fulltext_search_idx ON {} USING GIN(title gin_trgm_ops);".format(Literature._meta.db_table),
            reverse_sql="DROP INDEX literature_title_fulltext_search_idx;"
        ),
    ]