# Generated by Django 3.2 on 2022-03-17 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
        ('bareme', '0008_alter_regime_bareme'),
    ]

    operations = [
        migrations.AddField(
            model_name='regime',
            name='parc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.parc'),
        ),
        migrations.AlterField(
            model_name='regime',
            name='bareme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bareme.bareme'),
        ),
    ]
