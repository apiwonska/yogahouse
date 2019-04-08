from django.contrib import admin
from .models import Post, Category

# Register your models here.
class PostAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'updated']

class CategoryAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'updated']
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)