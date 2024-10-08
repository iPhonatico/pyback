# Generated by Django 5.1.1 on 2024-09-08 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_alter_reservation_parkingschedule'),
        ('organization', '0008_parking_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='parkingSchedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.parkingschedule'),
        ),
    ]
