# Generated by Django 4.0.4 on 2022-04-25 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0003_box_parc'),
        ('app', '0017_sousarticle_dangereux'),
    ]

    operations = [
        migrations.AddField(
            model_name='sousarticle',
            name='box',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.box'),
        ),
    ]