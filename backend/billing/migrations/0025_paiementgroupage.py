# Generated by Django 4.0.3 on 2022-04-17 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
        ('billing', '0024_alter_ligneproformagroupage_quantite'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaiementGroupage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('mode', models.CharField(choices=[('Chèque', 'Chèque'), ('Espèce', 'Espèce')], max_length=50)),
                ('cheque', models.CharField(blank=True, max_length=50, null=True)),
                ('montant', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('banque', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.banque')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.facturegroupage')),
            ],
            options={
                'verbose_name_plural': 'paiements groupage',
            },
        ),
    ]
