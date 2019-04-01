from django.contrib import admin
from .models import Color, ClassType, Teacher, StartTime, ClassInSchedule

# Register your models here.

class ClassTypeAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'updated']

class TeacherAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'updated']

class ClassInScheduleAdmin(admin.ModelAdmin):
	readonly_fields = ['created', 'updated']

admin.site.register(Color)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StartTime)
admin.site.register(ClassInSchedule, ClassInScheduleAdmin)
