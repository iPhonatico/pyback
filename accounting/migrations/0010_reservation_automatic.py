# Generated by Django 5.1.1 on 2024-09-08 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_alter_reservation_parkingschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='automatic',
            field=models.BooleanField(default=False),
        ),
    ]
