# Generated by Django 2.1.4 on 2018-12-17 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_teacher_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='picture',
            new_name='image',
        ),
        migrations.AddField(
            model_name='aboutinfo',
            name='image',
            field=models.ImageField(default=1, upload_to='', verbose_name='Zdjęcie'),
            preserve_default=False,
        ),
    ]
