# Generated by Django 2.0.2 on 2018-03-07 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waittimes', '0008_delete_patientwaittime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencydept',
            name='predicted_wait',
            field=models.CharField(default='', max_length=20),
        ),
    ]
