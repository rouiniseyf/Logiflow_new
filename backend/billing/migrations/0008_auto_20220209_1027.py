# Generated by Django 3.2 on 2022-02-09 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20220202_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproforma',
            name='REMISE',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='proforma',
            name='REMISE',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True),
        ),
    ]
