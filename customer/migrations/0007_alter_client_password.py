# Generated by Django 5.1.1 on 2024-09-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_client_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
