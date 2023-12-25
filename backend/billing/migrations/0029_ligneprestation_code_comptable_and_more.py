# Generated by Django 4.2.5 on 2023-10-01 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0024_bareme_accostage_historicalbareme_accostage'),
        ('billing', '0028_auto_20221005_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligneprestation',
            name='code_comptable',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ligneprestation',
            name='rubrique_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rubrique_prestation', to='bareme.rubrique'),
        ),
        migrations.AddField(
            model_name='ligneproformagroupage',
            name='code_comptable',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ligneproformagroupage',
            name='rubrique_object',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bareme.rubrique'),
        ),
    ]
