# Generated by Django 4.0.3 on 2022-04-14 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0017_proformagroupage_date_proforma'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proformagroupage',
            old_name='total_debeur',
            new_name='DEBEUR',
        ),
        migrations.AddField(
            model_name='proformagroupage',
            name='debeur',
            field=models.BooleanField(default=False, verbose_name='DEBEUR'),
        ),
    ]
