# Generated by Django 5.0.3 on 2024-12-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamanage', '0005_alter_pic_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='image',
            field=models.ImageField(upload_to='uploaded_images'),
        ),
    ]