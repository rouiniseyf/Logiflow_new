# Generated by Django 4.0.3 on 2022-04-13 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0011_alter_facturegroupage_options_proformagroupage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturegroupage',
            name='article',
        ),
        migrations.RemoveField(
            model_name='facturegroupage',
            name='gros',
        ),
        migrations.RemoveField(
            model_name='facturegroupage',
            name='sous_article',
        ),
    ]
