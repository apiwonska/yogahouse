from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models


class ClassOffer(models.Model):

    title = models.CharField(max_length=100, verbose_name='nazwa zajęć')
    description = models.TextField(max_length=2000, verbose_name='opis zajęć')
    order = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='kolejność wyświetlania')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'zajęcia'
        verbose_name_plural = 'zajęcia w ofercie'
        ordering = ['order']

    def __str__(self):
        return self.title


class PriceCategory(models.Model):

    TWO = '2'
    THREE = '3'

    ITEMS_IN_ROW_CHOICES = (
        (TWO, '2'),
        (THREE, '3')
    )

    name = models.CharField(max_length=100, verbose_name='nazwa cennika')
    class_duration = models.PositiveSmallIntegerField(
        verbose_name='czas trwania zajęć [min]')
    items_in_row = models.CharField(max_length=1, choices=ITEMS_IN_ROW_CHOICES,
                                    default=THREE, verbose_name='liczba wyświetlanych kart w rzędzie')

    order = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='kolejność wyświetlania')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'cennik - kategoria'
        verbose_name_plural = 'cenniki - kategorie'
        ordering = ['order']

    def __str__(self):
        return self.name


class PriceDetail(models.Model):

    description = models.CharField(
        max_length=100, verbose_name='dodatkowe informacje')
    order = models.PositiveSmallIntegerField(
        verbose_name='kolejność wyświetlania')

    class Meta:
        verbose_name = 'karnet - szczegółowa informacja'
        verbose_name_plural = 'cenniki - karnety - szczegółowe informacje'
        ordering = ['order']

    def __str__(self):
        return self.description


class PriceOption(models.Model):

    name = models.CharField(max_length=100, verbose_name='nazwa karnetu')
    price = models.PositiveSmallIntegerField(verbose_name='cena')

    price_category = models.ForeignKey(
        PriceCategory,
        on_delete=models.CASCADE,
        verbose_name='nazwa cennika')
    details = models.ManyToManyField(
        PriceDetail,
        blank=True,
        verbose_name='szczegóły',
        related_name='get_price_option'
    )

    order = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='kolejność wyświetlania')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'cennik - karnet'
        verbose_name_plural = 'cennki - karnety'
        ordering = ['order']

    def __str__(self):
        return self.name


class Conditions(models.Model):

    title = models.CharField(max_length=100, verbose_name='tytuł')
    content = RichTextField(verbose_name='treść')

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'regulamin'
        verbose_name_plural = 'regulamin'

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        if Conditions.objects.all().exclude(pk=self.pk).exists():
            raise ValidationError(
                'Może być tylko jeden obiekt "Regulamin". Usuń istniejący obiekt, jeśli chcesz dodać nowy.')
