# Generated by Django 5.1.1 on 2024-09-08 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_user_address_user_identification_user_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='identification',
            field=models.CharField(max_length=10),
        ),
    ]
