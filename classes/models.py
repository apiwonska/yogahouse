from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

# ------ CLASSES ---------

class ClassOffer(models.Model):
	title = models.CharField(max_length=100, verbose_name='Nazwa zajęć')
	description = models.TextField(max_length=2000, verbose_name='Opis zajęć')
	order = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kolejność wyświetlania')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Zajęcia'
		verbose_name_plural='Zajęcia w ofercie'
		ordering = ['order']

	def __str__(self):
		return self.title

# ------ PRICES ---------

class PriceCategory(models.Model):

	TWO = '2'
	THREE = '3'

	ITEMS_IN_ROW_CHOICES = (
		(TWO,'2'),
		(THREE,'3')
		)

	name = models.CharField(max_length=100, verbose_name='Nazwa cennika')
	class_duration = models.PositiveSmallIntegerField(verbose_name='Czas trwania zajęć [min]')
	items_in_row = models.CharField(max_length=1, choices=ITEMS_IN_ROW_CHOICES, default=THREE, verbose_name='Liczba wyświetlanych kart w rzędzie')

	order = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kolejność wyświetlania')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Cennik - Kategoria'
		verbose_name_plural = 'Cenniki - Kategorie'
		ordering = ['order']

	def __str__(self):
		return self.name

class PriceDetail(models.Model):
	description = models.CharField(max_length=100, verbose_name='Dodatkowe informacje')
	order = models.PositiveSmallIntegerField(verbose_name='Kolejność wyświetlania')

	class Meta:
		verbose_name = 'Karnet - szczegółowa informacja'
		verbose_name_plural = 'Cenniki - Karnety - szczegółowe informacje'
		ordering = ['order']

	def __str__(self):
		return self.description

class PriceOption(models.Model):
	name = models.CharField(max_length=100 ,verbose_name='Nazwa karnetu')
	price = models.PositiveSmallIntegerField(verbose_name='Cena')

	price_category = models.ForeignKey(
		PriceCategory, 
		on_delete=models.CASCADE, 
		verbose_name='Nazwa Cennika')
	details = models.ManyToManyField(
		PriceDetail, 
		blank=True,
		verbose_name='Szczegóły',
		related_name='get_price_option'
		)

	order = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Kolejność wyświetlania')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name = 'Cennik - Karnet'
		verbose_name_plural = 'Cennki - Karnety'
		ordering = ['order']

	def __str__(self):
		return self.name



# ------ CONDITIONS ---------

class Conditions(models.Model):
	title = models.CharField(max_length=100, verbose_name='Tytuł')
	content = RichTextField(verbose_name='Treść')

	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name = 'Regulamin'
		verbose_name_plural = 'Regulamin'

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if Conditions.objects.exists() and not self.pk:
			raise ValidationError('Może być tylko jeden obiekt "Regulamin".')
		return super(Conditions, self).save(*args,**kwargs)