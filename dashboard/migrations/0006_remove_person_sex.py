# Generated by Django 2.2.1 on 2019-06-13 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20190613_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='sex',
        ),
    ]
