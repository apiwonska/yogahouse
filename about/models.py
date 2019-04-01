from django.db import models

# Create your models here.
class AboutInfo(models.Model):
	presentation = models.TextField(max_length=2000, verbose_name='Prezentacja')
	image = models.ImageField(
		upload_to = 'img/about',
		verbose_name='Zdjęcie')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='O Nas'
		verbose_name_plural='O Nas'

	def __str__(self):
		return 'Prezentacja'

	def save(self, *args, **kwargs):
		if AboutInfo.objects.exists() and not self.pk:
			raise ValidationError('Może być tylko jeden obiekt "Prezentacja". Jeśli chcesz zmienić opis w sekcji "O Nas", zaktualizuj istniejący obiekt.')
		return super(AboutInfo, self).save(*args,**kwargs)

class Teacher(models.Model):
	name = models.CharField(max_length=200, verbose_name='Imię i nazwisko')
	description = models.TextField(max_length=2000, verbose_name='Opis')
	image = models.ImageField(
		upload_to = 'img/about',
		verbose_name='Zdjęcie')
	order = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kolejność')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name = 'Instruktor'
		verbose_name_plural = 'Instruktorzy'
		ordering = ['order']

	def __str__(self):
		return self.name
