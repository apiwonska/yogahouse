# Generated by Django 2.1.4 on 2018-12-20 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Tytuł')),
                ('date_start', models.DateTimeField(verbose_name='Data rozpoczęcia wydarzenia')),
                ('date_end', models.DateTimeField(verbose_name='Data zakończenia wydarzenia')),
                ('place', models.CharField(max_length=100, verbose_name='Miejsce wydarzenia')),
                ('desciption', models.TextField(verbose_name='Opis wydarzenia')),
                ('image', imagekit.models.fields.ProcessedImageField(default='events/img/event_default.jpg', upload_to='img/events', verbose_name='Zdjęcie')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Dodane przez')),
            ],
            options={
                'verbose_name': 'Wydarzenie',
                'verbose_name_plural': 'Wydarzenia',
                'ordering': ['date_start'],
            },
        ),
    ]
