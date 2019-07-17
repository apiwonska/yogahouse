from django.core.exceptions import ValidationError
from django.db import models


class AboutInfo(models.Model):

    presentation = models.TextField(
        max_length=2000, verbose_name='prezentacja')
    image = models.ImageField(
        upload_to='img/about',
        verbose_name='zdjęcie')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'o nas'
        verbose_name_plural = 'o nas'

    def __str__(self):
        return 'Prezentacja'

    def clean(self):
        if AboutInfo.objects.exists() and not self.pk:
            raise ValidationError('Może być tylko jeden obiekt "Prezentacja". '
                                  'Jeśli chcesz zmienić opis w sekcji "O Nas", zaktualizuj istniejący obiekt.')


class Teacher(models.Model):

    name = models.CharField(max_length=200, verbose_name='imię i nazwisko')
    description = models.TextField(max_length=2000, verbose_name='opis')
    image = models.ImageField(
        upload_to='img/about',
        verbose_name='zdjęcie')
    order = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='kolejność')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'instruktor'
        verbose_name_plural = 'instruktorzy'
        ordering = ['order']

    def __str__(self):
        return self.name
