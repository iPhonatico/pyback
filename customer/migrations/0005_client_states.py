# Generated by Django 5.1.1 on 2024-09-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_rename_indentification_client_identification'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='states',
            field=models.BooleanField(default=True),
        ),
    ]
