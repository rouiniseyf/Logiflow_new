# Generated by Django 4.2.5 on 2023-10-01 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0030_commande_rubrique_object_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligneprestationarticle',
            name='code_comptable',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]