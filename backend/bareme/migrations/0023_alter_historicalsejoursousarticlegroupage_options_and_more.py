# Generated by Django 4.2.2 on 2023-09-18 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0022_sejoursousarticlegroupage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalsejoursousarticlegroupage',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical sejour sous article groupage', 'verbose_name_plural': 'historical séjours Sous article'},
        ),
        migrations.AlterModelOptions(
            name='sejoursousarticlegroupage',
            options={'ordering': ['id'], 'verbose_name_plural': 'séjours Sous article'},
        ),
    ]
