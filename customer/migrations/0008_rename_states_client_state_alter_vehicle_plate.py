# Generated by Django 5.1.1 on 2024-09-05 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_alter_client_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='states',
            new_name='state',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='plate',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
