from django.contrib import admin

from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated', 'was_published']
    fieldsets = (
        (None, {'fields': ('title', 'content', 'image')}),
        ('Informacje dodatkowe', {
         'fields': (('category', 'author'), 'was_published')}),
        ('Data utworzenia/ edycji/ publikacji',
            {
                'fields': ('published', 'created', 'updated'),
                'classes': ('collapse',),
                'description': 'W momencie tworzenia postu, data publikacji nie powinna być w przeszłości.'
            }
         ),
    )

    list_display = ('title', 'author', 'was_published',
                    'published', 'post_categories')
    list_filter = ['published', 'author', 'category']
    search_fields = ('title', 'content')
    date_hierarchy = 'published'

    def post_categories(self, obj):
        return ', '.join([c.name for c in obj.category.all().order_by('name')])
    post_categories.short_description = 'Kategoria'


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'updated']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
