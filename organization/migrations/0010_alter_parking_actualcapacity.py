# Generated by Django 5.1.1 on 2024-09-08 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_parking_actualcapacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='actualCapacity',
            field=models.PositiveIntegerField(),
        ),
    ]
