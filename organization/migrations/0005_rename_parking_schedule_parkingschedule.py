# Generated by Django 5.1.1 on 2024-09-08 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_rename_horario_parking_schedule_schedule'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Parking_schedule',
            new_name='ParkingSchedule',
        ),
    ]
