# Generated by Django 5.0.3 on 2024-12-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='ph',
            new_name='input_ph',
        ),
        migrations.RemoveField(
            model_name='data',
            name='ec',
        ),
        migrations.AddField(
            model_name='data',
            name='drain_ec',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='drain_ph',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='drain_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='input_ec',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='input_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='plant_weight',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='soil_EC',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='soil_humidity',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='soil_pH',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='soil_temperature',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]