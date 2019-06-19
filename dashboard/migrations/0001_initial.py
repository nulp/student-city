# Generated by Django 2.2 on 2019-05-16 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BookNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=16)),
                ('address', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.District')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Pasportyst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeLocality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('short', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Country')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PersonHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.PositiveIntegerField(db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('data', models.TextField()),
                ('edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('surname', models.CharField(db_index=True, max_length=128)),
                ('patronymic', models.CharField(blank=True, db_index=True, default='', max_length=128)),
                ('birthday', models.DateField(db_index=True)),
                ('unique_number', models.CharField(blank=True, max_length=256, null=True)),
                ('passport_number', models.CharField(max_length=32, null=True)),
                ('passport_authority', models.CharField(max_length=128, null=True)),
                ('date_of_issue', models.DateField(null=True)),
                ('registered_date', models.DateField(db_index=True, null=True)),
                ('de_registered_date', models.DateField(blank=True, db_index=True, null=True)),
                ('new_address', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('number_in_book', models.IntegerField(blank=True, default=0)),
                ('room', models.CharField(blank=True, max_length=32, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_time', models.DateTimeField(auto_now=True)),
                ('note', models.TextField(blank=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Book')),
                ('created_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persons_created', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('hostel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Hostel')),
                ('locality', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Locality')),
                ('pasportyst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Pasportyst')),
                ('updated_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persons_updated', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('people', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='locality',
            name='l_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.TypeLocality'),
        ),
        migrations.AddField(
            model_name='locality',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Region'),
        ),
        migrations.AddField(
            model_name='district',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Region'),
        ),
        migrations.CreateModel(
            name='DeletedPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.PositiveIntegerField(db_index=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('deleted_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book_number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.BookNumber'),
        ),
        migrations.AddField(
            model_name='book',
            name='hostel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Hostel'),
        ),
        migrations.AddField(
            model_name='book',
            name='pasportyst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.Pasportyst'),
        ),
    ]
