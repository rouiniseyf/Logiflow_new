# Generated by Django 4.0.3 on 2022-04-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0019_remove_ligneprestationgroupage_debeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturegroupage',
            name='DEBEUR',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
