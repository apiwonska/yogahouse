from django.contrib import admin
from django.db import models
from django.forms import TextInput

from .forms import ClassOccurrenceForm
from .models import ClassOccurrence, ClassType, Course, Teacher


class ClassTypeAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'description', 'color']
    readonly_fields = ['slug', 'created', 'updated']


class TeacherAdmin(admin.ModelAdmin):

    readonly_fields = ['created', 'updated']


class CourseAdmin(admin.ModelAdmin):

    list_display = ('weekday', 'start_time', 'name', 'teacher', 'active')
    list_filter = ['active', 'weekday', 'class_type__name', 'teacher__name']
    fieldsets = (
        ('Informacje ogólne:', {
            'fields': ('class_type', 'name', 'teacher'),
        }),
        ('Czas:', {
            'fields': ('weekday', 'start_time', 'duration'),
        }),
        ('Informacje dodatkowe:', {
            'fields': ('active', 'note', 'max_number_of_students'),
        }),
        (None, {
            'fields': ('created', 'updated'),
        }),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '200'})},
    }
    readonly_fields = ['end_time', 'created', 'updated']


class ClassOccurrenceAdmin(admin.ModelAdmin):
    form = ClassOccurrenceForm
    save_on_top = True
    save_on_bottom = False
    search_fields = ['course__name', ]
    list_display = ['date', 'week_number', 'weekday', 'start_time', 'get_course_name',
                    'main_teacher', 'substitute', 'number_of_students', 'number_of_places_left', 'status']
    list_filter = ['cancelled', 'course__name', 'course__teacher']
    date_hierarchy = 'date'
    fieldsets = (
        ('Informacje podstawowe:', {
            'fields': ('course', ('date', 'start_time'), 'main_teacher', 'substitute_teacher',),
        }),
        ('Informacje dodatkowe:', {
            'fields': ('note', 'cancelled'),
        }),
        ('Lista uczestników:', {
            'fields': ('students', 'number_of_students', 'number_of_places_left'),
        }),
        (None, {
            'fields': ('created', 'updated'),
        }),
    )
    filter_horizontal = ('students',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '200'})},
    }
    readonly_fields = ['start_time', 'end_time', 'main_teacher',
                       'number_of_students', 'number_of_places_left', 'created', 'updated']

    def week_number(self, obj):
        return obj.date.isocalendar()[1]
    week_number.short_description = 'tydzień'

    def weekday(self, obj):
        return obj.date.strftime('%A')
    weekday.short_description = 'dzień tygodnia'

    def get_course_name(self, obj):
        return obj.course.name
    get_course_name.short_description = 'nazwa kursu'

    def substitute(self, obj):
        if obj.substitute_teacher:
            return 'Z'
    substitute.short_description = 'zastępstwo'


admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ClassOccurrence, ClassOccurrenceAdmin)
