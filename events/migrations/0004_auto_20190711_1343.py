# Generated by Django 2.1.4 on 2019-07-11 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20181221_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date_start'], 'verbose_name': 'wydarzenie', 'verbose_name_plural': 'wydarzenia'},
        ),
        migrations.AlterField(
            model_name='event',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='dodane przez'),
        ),
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateTimeField(verbose_name='czas zakończenia wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateTimeField(verbose_name='czas rozpoczęcia wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='opis wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=100, verbose_name='miejsce wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200, verbose_name='tytuł'),
        ),
        migrations.AlterField(
            model_name='event',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='data aktualizacji'),
        ),
    ]
