# Generated by Django 3.2 on 2022-01-25 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20220118_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproforma',
            name='trashed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='proforma',
            name='trashed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]