# Generated by Django 4.0.3 on 2022-04-14 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0023_rename_lignefacturegroupage_ligneproformagroupage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ligneproformagroupage',
            name='quantite',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
