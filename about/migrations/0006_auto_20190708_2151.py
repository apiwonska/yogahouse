# Generated by Django 2.1.4 on 2019-07-08 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0005_auto_20181217_2110'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutinfo',
            options={'verbose_name': 'o nas', 'verbose_name_plural': 'o nas'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['order'], 'verbose_name': 'instruktor', 'verbose_name_plural': 'instruktorzy'},
        ),
        migrations.AlterField(
            model_name='aboutinfo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='aboutinfo',
            name='image',
            field=models.ImageField(upload_to='img/about', verbose_name='zdjęcie'),
        ),
        migrations.AlterField(
            model_name='aboutinfo',
            name='presentation',
            field=models.TextField(max_length=2000, verbose_name='prezentacja'),
        ),
        migrations.AlterField(
            model_name='aboutinfo',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='data aktualizacji'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='description',
            field=models.TextField(max_length=2000, verbose_name='opis'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(upload_to='img/about', verbose_name='zdjęcie'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=200, verbose_name='imię i nazwisko'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='order',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='kolejność'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='data aktualizacji'),
        ),
    ]
