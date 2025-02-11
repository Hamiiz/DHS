# Generated by Django 4.2.18 on 2025-02-09 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_managment', '0006_rename_id_appointment__id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='payment',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_managment.appointment'),
        ),
    ]
