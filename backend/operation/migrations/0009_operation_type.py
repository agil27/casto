# Generated by Django 2.2.3 on 2019-09-08 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0008_auto_20190908_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='type',
            field=models.CharField(default='', max_length=128),
        ),
    ]
