# Generated by Django 5.0.3 on 2024-12-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanage', '0007_data_co2_data_plant_weight2_data_prep_f1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='drain_ec2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='drain_ph2',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='drain_weight2',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='input_ec2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='input_ph2',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='input_weight2',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
