# Generated by Django 5.1.1 on 2024-09-05 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_rename_taxid_client_indentification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='indentification',
            new_name='identification',
        ),
    ]
