# Generated by Django 2.0.2 on 2018-02-23 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waittimes', '0003_auto_20180218_1809'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.RemoveField(
            model_name='emergencydept',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='emergencydept',
            name='location',
        ),
        migrations.AddField(
            model_name='emergencydept',
            name='driving_time',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='emergencydept',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='emergencydept',
            name='lng',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='emergencydept',
            name='msa',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='emergencydept',
            name='predicted_wait',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patientwaittime',
            name='metro_area',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='urgentcare',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='urgentcare',
            name='lng',
            field=models.FloatField(default=0),
        ),
    ]
