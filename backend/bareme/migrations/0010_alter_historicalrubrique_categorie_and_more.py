# Generated by Django 4.0.3 on 2022-04-11 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0009_auto_20220317_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrubrique',
            name='categorie',
            field=models.CharField(blank=True, choices=[('Automatique', 'Automatique'), ('Clarck Intégral', 'Clarck Intégral'), ('Clarck Partiel', 'Clarck Partiel'), ('Dangereux', 'Dangereux'), ('Dépotage', 'Dépotage'), ('Manutentions humaines Intégral', 'Manutentions humaines Intégral'), ('Manutentions humaines Partiel', 'Manutentions humaines Partiel'), ('Préstation occasionnelle', 'Préstation occasionnelle'), ('Scanner', 'Scanner'), ('Visite', 'Visite'), ('Groupage', 'Groupage')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='rubrique',
            name='categorie',
            field=models.CharField(blank=True, choices=[('Automatique', 'Automatique'), ('Clarck Intégral', 'Clarck Intégral'), ('Clarck Partiel', 'Clarck Partiel'), ('Dangereux', 'Dangereux'), ('Dépotage', 'Dépotage'), ('Manutentions humaines Intégral', 'Manutentions humaines Intégral'), ('Manutentions humaines Partiel', 'Manutentions humaines Partiel'), ('Préstation occasionnelle', 'Préstation occasionnelle'), ('Scanner', 'Scanner'), ('Visite', 'Visite'), ('Groupage', 'Groupage')], max_length=30, null=True),
        ),
    ]
