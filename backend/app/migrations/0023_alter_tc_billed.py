# Generated by Django 3.2.16 on 2022-10-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20221005_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tc',
            name='billed',
            field=models.BooleanField(default=False),
        ),
    ]
