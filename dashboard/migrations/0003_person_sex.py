# Generated by Django 2.2.1 on 2019-06-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20190611_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='sex',
            field=models.CharField(default='Ч', max_length=1),
        ),
    ]
