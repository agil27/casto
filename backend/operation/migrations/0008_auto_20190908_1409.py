# Generated by Django 2.2.3 on 2019-09-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0007_operation_processed_image_crop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='processed_image_crop',
            new_name='crop',
        ),
        migrations.RenameField(
            model_name='operation',
            old_name='processed_image',
            new_name='emotion',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='net',
        ),
        migrations.AddField(
            model_name='operation',
            name='gender',
            field=models.CharField(default='', max_length=128),
        ),
    ]
