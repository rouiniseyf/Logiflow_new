# Generated by Django 3.2 on 2022-02-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bareme', '0002_regime'),
    ]

    operations = [
        migrations.AddField(
            model_name='regime',
            name='enterposage',
            field=models.CharField(choices=[('hard', 'hard'), ('easy', 'easy')], default=1, max_length=5),
        ),
    ]