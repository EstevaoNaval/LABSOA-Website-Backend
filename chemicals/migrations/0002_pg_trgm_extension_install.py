from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('chemicals', '0001_initial')
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS pg_trgm;",
            reverse_sql="DROP EXTENSION IF EXISTS pg_trgm"
        ),
    ]
