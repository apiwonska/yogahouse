from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Event(models.Model):
	title = models.CharField(max_length=200 , verbose_name='Tytuł')
	date_start = models.DateTimeField(verbose_name='Data rozpoczęcia wydarzenia')
	date_end = models.DateTimeField(verbose_name='Data zakończenia wydarzenia')
	place = models.CharField(max_length=100, verbose_name='Miejsce wydarzenia')
	description = models.TextField(verbose_name='Opis wydarzenia')
	image = ProcessedImageField(
		upload_to = 'img/events',
		processors=[ResizeToFill(920,460)],
		format='JPEG',
		options={'quality':60},
		default = 'img/events/event_default.jpg',
		verbose_name='Zdjęcie')
	image_thumbnail = ImageSpecField(
		source='image',
		processors=[ResizeToFill(400,200)],
		format='JPEG',
		options={'quality':60})

	added_by = models.ForeignKey(
		User,
		verbose_name='Dodane przez',
		on_delete=models.CASCADE)

	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name = 'Wydarzenie'
		verbose_name_plural = 'Wydarzenia'
		ordering = ['date_start']

	def __str__(self):
		return self.title

	def description_short(self):
		description_short_words = self.description.split(' ')[:30]
		return ' '.join(description_short_words)

	def duration(self):
		return date_end.date()-date_start.date()+1
			

	# def clean_date_start(self):
	# 	date_start = self.cleaned_data.get('date_start')
	# 	if date_start < datetime.date.today():
	# 		raise ValidationError("Data rozpoczęcia nie może być w przeszłości!")
	# return date_start

	# def clean_date_end(self):
	# 	date_start = self.cleaned_data.get('date_start')
	# 	date_end = self.cleaned_data.get('date_end')
	# 	if date_end < date_start:
	# 		raise ValidationError("Data zakończenia musi być późniejsza niż data rozpoczęcia.")
	# return date_end