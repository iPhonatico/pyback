# Generated by Django 5.1.1 on 2024-09-08 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_alter_parking_actualcapacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkingschedule',
            name='available',
        ),
    ]
