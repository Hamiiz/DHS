# Generated by Django 4.2.18 on 2025-02-09 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_managment', '0005_alter_appointment_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='id',
            new_name='_id',
        ),
    ]
