from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Event(models.Model):

    title = models.CharField(max_length=200, verbose_name='tytuł')
    date_start = models.DateTimeField(
        verbose_name='czas rozpoczęcia wydarzenia')
    date_end = models.DateTimeField(verbose_name='czas zakończenia wydarzenia')
    place = models.CharField(max_length=100, verbose_name='miejsce wydarzenia')
    description = models.TextField(verbose_name='opis wydarzenia')
    image = ProcessedImageField(
        upload_to='img/events',
        processors=[ResizeToFill(920, 460)],
        format='JPEG',
        options={'quality': 60},
        default='img/events/event_default.jpg',
        verbose_name='Zdjęcie')
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 200)],
        format='JPEG',
        options={'quality': 60})

    added_by = models.ForeignKey(
        User,
        verbose_name='dodane przez',
        on_delete=models.CASCADE)

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'wydarzenie'
        verbose_name_plural = 'wydarzenia'
        ordering = ['date_start']

    def __str__(self):
        return self.title

    @property
    def description_short(self):
        description_short_words = self.description.split(' ')[:30]
        return ' '.join(description_short_words)

    @property
    def duration(self):
        return (self.date_end.date() - self.date_start.date()).days + 1

    def clean(self, *args, **kwargs):
        if self.date_start < timezone.now():
            raise ValidationError(
                {'date_start': [
                    'Czas rozpoczęcia nie może być w przeszłości!'
                ]})
        if self.date_end < self.date_start:
            raise ValidationError(
                {'date_end': [
                    'Czas zakończenia nie może być wcześniejszy niż czas rozpoczęcia.'
                ]})
