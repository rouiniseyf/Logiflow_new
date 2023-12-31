# Generated by Django 4.2.2 on 2023-09-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0023_alter_historicalsejoursousarticlegroupage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bareme',
            name='accostage',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name="à partir de la date d'accostage"),
        ),
        migrations.AddField(
            model_name='historicalbareme',
            name='accostage',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name="à partir de la date d'accostage"),
        ),
    ]
