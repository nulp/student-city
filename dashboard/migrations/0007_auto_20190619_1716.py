# Generated by Django 2.2.1 on 2019-06-19 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_person_sex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['hostel_id', 'number']},
        ),
        migrations.RenameField(
            model_name='locality',
            old_name='l_type',
            new_name='type_locality',
        ),
        migrations.AlterField(
            model_name='person',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]