# Generated by Django 4.2.5 on 2023-10-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0033_alter_historicalproforma_entreposage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proformagroupage',
            name='enterposage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
