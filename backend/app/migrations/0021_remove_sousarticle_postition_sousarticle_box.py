# Generated by Django 4.0.4 on 2022-04-27 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0003_box_parc'),
        ('app', '0020_remove_sousarticle_box_sousarticle_postition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sousarticle',
            name='postition',
        ),
        migrations.AddField(
            model_name='sousarticle',
            name='box',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.box'),
        ),
    ]