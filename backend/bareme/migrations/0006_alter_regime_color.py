# Generated by Django 3.2 on 2022-02-16 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0005_regime_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regime',
            name='color',
            field=models.CharField(choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('success', 'Success'), ('danger', 'Danger'), ('warning', 'Warning'), ('info', 'Info'), ('light', 'Light'), ('dark', 'Dark')], max_length=50, null=True),
        ),
    ]