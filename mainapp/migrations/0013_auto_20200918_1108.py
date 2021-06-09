# Generated by Django 3.1.1 on 2020-09-18 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20200911_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='specialty',
            field=models.CharField(choices=[('General practice', 'General practice'), ('Clinical radiology', 'Clinical radiology'), ('Anaesthesia', 'Anaesthesia'), ('Ophthalmology', 'Ophthalmology')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='mainapp.patient'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='consultation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.consultation'),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='consultation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.consultation'),
        ),
    ]