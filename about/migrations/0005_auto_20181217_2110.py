# Generated by Django 2.1.4 on 2018-12-17 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0004_auto_20181217_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutinfo',
            name='image',
            field=models.ImageField(upload_to='img/about', verbose_name='Zdjęcie'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(upload_to='img/about', verbose_name='Zdjęcie'),
        ),
    ]
