# Generated by Django 4.2.5 on 2023-10-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0026_alter_historicalprestationoccasionnelle_prix_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprestationoccasionnelle',
            name='prix',
            field=models.DecimalField(decimal_places=3, max_digits=19),
        ),
        migrations.AlterField(
            model_name='prestationoccasionnelle',
            name='prix',
            field=models.DecimalField(decimal_places=3, max_digits=19),
        ),
    ]
