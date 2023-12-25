# Generated by Django 3.2 on 2022-02-02 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0002_regime'),
        ('app', '0006_auto_20220118_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gros',
            name='methode_calcule',
        ),
        migrations.AddField(
            model_name='gros',
            name='regeme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bareme.regime'),
        ),
    ]
