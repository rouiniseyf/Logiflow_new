# Generated by Django 3.2 on 2022-01-18 13:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reference', '0001_initial'),
        ('bareme', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalgros',
            name='bareme',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bareme.bareme'),
        ),
        migrations.AddField(
            model_name='historicalgros',
            name='consignataire',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.consignataire'),
        ),
        migrations.AddField(
            model_name='historicalgros',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalgros',
            name='navire',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.navire'),
        ),
        migrations.AddField(
            model_name='historicalgros',
            name='port_emission',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.port'),
        ),
        migrations.AddField(
            model_name='historicalgros',
            name='port_reception',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.port'),
        ),
        migrations.AddField(
            model_name='historicalbulletinsescort',
            name='charge_chargement',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbulletinsescort',
            name='charge_reception',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalbulletinsescort',
            name='gros',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.gros'),
        ),
        migrations.AddField(
            model_name='historicalbulletinsescort',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalarticle',
            name='client',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.client'),
        ),
        migrations.AddField(
            model_name='historicalarticle',
            name='gros',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='app.gros'),
        ),
        migrations.AddField(
            model_name='historicalarticle',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalarticle',
            name='transitaire',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='reference.transitaire'),
        ),
        migrations.AddField(
            model_name='gros',
            name='armateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.armateur'),
        ),
        migrations.AddField(
            model_name='gros',
            name='bareme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bareme.bareme'),
        ),
        migrations.AddField(
            model_name='gros',
            name='consignataire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.consignataire'),
        ),
        migrations.AddField(
            model_name='gros',
            name='navire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.navire'),
        ),
        migrations.AddField(
            model_name='gros',
            name='port_emission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='port_emission', to='reference.port'),
        ),
        migrations.AddField(
            model_name='gros',
            name='port_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='port_reception', to='reference.port'),
        ),
        migrations.AddField(
            model_name='bulletinsescort',
            name='charge_chargement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='agent_charge_chargement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bulletinsescort',
            name='charge_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='agent_charge_creation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bulletinsescort',
            name='gros',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.gros'),
        ),
        migrations.AddField(
            model_name='article',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reference.client'),
        ),
        migrations.AddField(
            model_name='article',
            name='gros',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.gros'),
        ),
        migrations.AddField(
            model_name='article',
            name='transitaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='reference.transitaire'),
        ),
        migrations.AlterUniqueTogether(
            name='gros',
            unique_together={('numero', 'accostage')},
        ),
    ]