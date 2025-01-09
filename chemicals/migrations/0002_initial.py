# Generated by Django 5.1 on 2025-01-08 21:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chemicals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chemical',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chemicals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conformation',
            name='chemical',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conformations', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='druglikerule',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='druglike_rules', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='identifier',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='chemical',
            name='literature',
            field=models.ManyToManyField(related_name='chemicals', to='chemicals.literature'),
        ),
        migrations.AddField(
            model_name='p450inhibition',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='p450_inhibitors', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='partitioncoefficient',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='partition_coefficients', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='pharmacokinetics',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pharmacokinetics', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='physicalproperty',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='physical_properties', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='physicochemicalproperty',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='physicochemical_properties', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='qsarscore',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='qsar_scores', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='solubility',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='solubilities', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='synonym',
            name='chemical',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synonyms', to='chemicals.chemical'),
        ),
        migrations.AddField(
            model_name='undesirablesubstructurealert',
            name='chemical',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='undesirable_substructure_alerts', to='chemicals.chemical'),
        ),
    ]
