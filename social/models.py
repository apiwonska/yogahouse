from django.db import models


class Link(models.Model):

    key = models.SlugField(max_length=100, unique=True,
                           verbose_name='Nazwa klucza')
    name = models.CharField(
        max_length=200, verbose_name='Sieć społecznościowa')
    url = models.URLField(max_length=200, null=True,
                          blank=True, verbose_name='Link')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Data aktualizacji')

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Linki'
        ordering = ['name']

    def __str__(self):
        return self.name
