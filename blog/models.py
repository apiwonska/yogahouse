from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, unique=True, verbose_name='Nazwa Kategorii')
	slug = models.SlugField(max_length=50, unique=True)

	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Kategoria'
		verbose_name_plural = 'Kategorie'
		ordering = ['name']

	def __str__(self):
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=200, verbose_name='Tytuł')
	content = RichTextField(verbose_name='Treść')
	image = ProcessedImageField(
		upload_to = 'img/blog',
		processors=[ResizeToFill(920,460)],
		format='JPEG',
		options={'quality':60},
		default = 'img/blog/blog_default.jpg',
		verbose_name='Zdjęcie')
	image_thumbnail = ImageSpecField(
		source='image',
		processors=[ResizeToFill(400,200)],
		format='JPEG',
		options={'quality':60})
	published = models.DateTimeField(verbose_name='Data publikacji', default=now)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		verbose_name='Autor')
	category = models.ManyToManyField(
		Category,
		verbose_name='Kategorie')

	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Post'
		verbose_name_plural='Posty'
		ordering = ['-created']

	def __str__(self):
		return self.title

	def was_published(self):
		return self.published < now()
	was_published.short_description = 'Opublikowano'
	was_published.boolean = True

	def content_short(self):
		content_short_words = self.content.split(' ')[:50]
		return ' '.join(content_short_words)