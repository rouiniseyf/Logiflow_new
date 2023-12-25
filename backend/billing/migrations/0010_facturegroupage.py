# Generated by Django 4.0.3 on 2022-04-13 08:08

import billing.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_sousarticle_date_depotage_and_more'),
        ('billing', '0009_auto_20220215_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactureGroupage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(default=billing.models.getNumeroFactureGroupage, max_length=9)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('HT', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('TVA', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('TTC', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('TR', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('timber', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('a_terme', models.BooleanField(default=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.article')),
                ('gros', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gros')),
                ('sous_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sousarticle')),
            ],
            options={
                'verbose_name_plural': 'factures',
                'ordering': ['-id'],
            },
        ),
    ]
