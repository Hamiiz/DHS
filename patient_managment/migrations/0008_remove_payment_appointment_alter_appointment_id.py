# Generated by Django 4.2.18 on 2025-02-09 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_managment', '0007_rename__id_appointment_id_alter_payment_appointment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='appointment',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
