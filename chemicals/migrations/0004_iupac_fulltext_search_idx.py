from django.db import migrations
from chemicals.models import Identifier

class Migration(migrations.Migration):

    dependencies = [
        ('chemicals','0003_pg_trgm_extension_install')
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE INDEX IF NOT EXISTS iupac_fulltext_search_idx ON {} USING GIN(iupac_name gin_trgm_ops);".format(Identifier._meta.db_table),
            reverse_sql="DROP INDEX iupac_fulltext_search_idx;"
        ),
    ]
