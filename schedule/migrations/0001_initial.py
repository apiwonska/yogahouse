# Generated by Django 2.1.4 on 2019-06-11 16:24

import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('about', '0005_auto_20181217_2110'),
        ('classes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassOccurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Data musi być w przyszłości i przypadać na dzień tygodnia, w którym odbywa się kurs', verbose_name='data')),
                ('start_time', models.TimeField(blank=True, verbose_name='godzina rozpoczęcia')),
                ('end_time', models.TimeField(blank=True, verbose_name='godzina zakończenia')),
                ('cancelled', models.BooleanField(default=False, verbose_name='anulowane')),
                ('note', models.CharField(blank=True, max_length=300, null=True, verbose_name='uwagi')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='data aktualizacji')),
            ],
            options={
                'verbose_name': 'Zaplanowane zajęcia',
                'verbose_name_plural': 'Zaplanowane zajęcia',
                'ordering': ['date', django.db.models.expressions.OrderBy(django.db.models.expressions.F('course'))],
            },
        ),
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa zajęć')),
                ('slug', models.SlugField(unique=True)),
                ('color', colorful.fields.RGBColorField(default='#007bff', verbose_name='Kolor')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')),
                ('description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.ClassOffer', verbose_name='Opis zajęć')),
            ],
            options={
                'verbose_name': 'Rodzaj zajęć',
                'verbose_name_plural': 'Rodzaje zajęć',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True, verbose_name='nazwa kursu')),
                ('weekday', models.CharField(choices=[('1_Poniedziałek', 'Poniedziałek'), ('2_Wtorek', 'Wtorek'), ('3_Środa', 'Środa'), ('4_Czwartek', 'Czwartek'), ('5_Piątek', 'Piątek'), ('6_Sobota', 'Sobota'), ('7_Niedziela', 'Niedziela')], max_length=14, verbose_name='dzień tygodnia')),
                ('start_time', models.TimeField(verbose_name='godzina rozpoczęcia')),
                ('end_time', models.TimeField(blank=True, verbose_name='godzina zakończenia')),
                ('duration', models.PositiveSmallIntegerField(default=55, verbose_name='czas trwania zajęć [min]')),
                ('active', models.BooleanField(default=True, verbose_name='aktywny')),
                ('note', models.CharField(blank=True, max_length=300, null=True, verbose_name='uwagi')),
                ('max_number_of_students', models.PositiveSmallIntegerField(default=30, verbose_name='Maksymalna liczba uczestników')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='data aktualizacji')),
                ('class_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.ClassType', verbose_name='rodzaj zajęć')),
            ],
            options={
                'verbose_name': 'kurs',
                'verbose_name_plural': 'kursy',
                'ordering': ['weekday', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Imię i nazwisko instruktora')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')),
                ('description', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='about.Teacher', verbose_name='Opis instruktora')),
            ],
            options={
                'verbose_name': 'Instruktor',
                'verbose_name_plural': 'Instruktorzy',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Teacher', verbose_name='instruktor prowadzący'),
        ),
        migrations.AddField(
            model_name='classoccurrence',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.Course', verbose_name='nazwa kursu'),
        ),
        migrations.AddField(
            model_name='classoccurrence',
            name='main_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_teacher_set', to='schedule.Teacher', verbose_name='instruktor'),
        ),
        migrations.AddField(
            model_name='classoccurrence',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='uczestnicy'),
        ),
        migrations.AddField(
            model_name='classoccurrence',
            name='substitute_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute_teacher_set', to='schedule.Teacher', verbose_name='zastępstwo'),
        ),
    ]
