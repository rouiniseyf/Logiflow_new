# Generated by Django 4.0.4 on 2022-04-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'boxs',
            },
        ),
    ]
