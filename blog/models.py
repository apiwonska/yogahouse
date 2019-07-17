from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill


class Category(models.Model):

    name = models.CharField(max_length=50, unique=True,
                            verbose_name='nazwa Kategorii')
    slug = models.SlugField(max_length=50, unique=True)

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'
        ordering = ['name']

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self._get_unique_slug()
        super(Category, self).save(*args, **kwargs)


class Post(models.Model):

    title = models.CharField(max_length=200, verbose_name='tytuł')
    content = RichTextField(verbose_name='treść')
    image = ProcessedImageField(
        upload_to='img/blog',
        processors=[ResizeToFill(920, 460)],
        format='JPEG',
        options={'quality': 60},
        default='img/blog/blog_default.jpg',
        verbose_name='zdjęcie')
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 200)],
        format='JPEG',
        options={'quality': 60})
    published = models.DateTimeField(
        verbose_name='data publikacji', default=now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='autor')
    category = models.ManyToManyField(
        Category,
        verbose_name='kategorie')

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:

        verbose_name = 'post'
        verbose_name_plural = 'posty'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def was_published(self):
        return self.published < now()
    was_published.short_description = 'Opublikowano'
    was_published.boolean = True
