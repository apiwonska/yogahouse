from django.contrib import admin

from .models import AboutInfo, Teacher


class AboutInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(AboutInfo)
admin.site.register(Teacher)
