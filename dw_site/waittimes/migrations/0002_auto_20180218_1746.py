# Generated by Django 2.0.2 on 2018-02-18 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waittimes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PatientWaittimes',
            new_name='PatientWaittime',
        ),
        migrations.RenameField(
            model_name='urgentcare',
            old_name='address_2',
            new_name='address2',
        ),
        migrations.RenameField(
            model_name='urgentcare',
            old_name='latitude',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='urgentcare',
            old_name='longitude',
            new_name='lng',
        ),
        migrations.RenameField(
            model_name='urgentcare',
            old_name='phone_number',
            new_name='telephone',
        ),
    ]