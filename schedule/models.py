from django.db import models
from colorful.fields import RGBColorField
from about.models import Teacher as TeacherDescription
from classes.models import ClassOffer as ClassDescription

class Color(models.Model):
	name = models.CharField(max_length=30)
	color = RGBColorField(default='#007bff', verbose_name='Kolor')

	class Meta:
		verbose_name='Kolor'
		verbose_name_plural='Kolory'

	def __str__(self):
		return self.name


class ClassType(models.Model):
	name = models.CharField(max_length=50, verbose_name='Nazwa zajęć')
	description = models.OneToOneField(ClassDescription, 
		on_delete=models.SET_NULL, 
		null=True, blank=True, 
		verbose_name='Opis zajęć'
	)
	display_color = models.ForeignKey(Color, 
		on_delete=models.SET_NULL, 
		null=True, blank=True, 
		verbose_name='Kolor wyświetlania'
	)	
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Rodzaj zajęć'
		verbose_name_plural = 'Rodzaje zajęć'

	def __str__(self):
		return self.name


class Teacher(models.Model):
	name = models.CharField(max_length=50, verbose_name='Imię i nazwisko instruktora')
	description = models.OneToOneField(TeacherDescription, 
		on_delete=models.SET_NULL, 
		null=True, blank=True, 
		verbose_name='Opis instruktora'
	)	
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

	class Meta:
		verbose_name='Instruktor'
		verbose_name_plural = 'Instruktorzy'

	def __str__(self):
		return self.name

class StartTime(models.Model):
	time = models.TimeField(verbose_name='Godzina rozpoczęcia')	
	
	class Meta:
		verbose_name='Godzina rozpoczęcia zajęć'
		verbose_name_plural='Godziny rozpoczęcia zajęć'

	def __str__(self):
		return str(self.time)

class ClassInSchedule(models.Model):
	MONDAY = "1_Poniedziałek"
	TUESDAY = "2_Wtorek"
	WEDNESDAY = "3_Środa"
	THURSDAY = "4_Czwartek"
	FRIDAY = "5_Piątek"
	SATURDAY = "6_Sobota"
	SUNDAY = "7_Niedziela"

	DAYS_OF_WEEK = (
		(MONDAY,"Poniedziałek"),
		(TUESDAY,"Wtorek"),
		(WEDNESDAY,"Środa"),
		(THURSDAY,"Czwartek"),
		(FRIDAY,"Piątek"),
		(SATURDAY,"Sobota"),
		(SUNDAY,"Niedziela"),
		)

	day_of_week = models.CharField(max_length=14, choices=DAYS_OF_WEEK, verbose_name='Dzień tygodnia' )
	start_time = models.ForeignKey(StartTime,
		on_delete=models.CASCADE,
		verbose_name='Godzina rozpoczęcia zajęć'
		)
	class_type = models.ForeignKey(ClassType, 
		on_delete=models.CASCADE, 
		verbose_name='Nazwa zajęć'
	)
	teacher = models.ForeignKey(Teacher, 
		on_delete=models.CASCADE, 
		verbose_name='Instruktor'
	)	
	created = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
	updated = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')
	
	class Meta:
		verbose_name = 'Zajęcia w Grafiku'
		verbose_name_plural = 'Zajęcia w Grafiku'
		ordering = ['day_of_week', 'start_time']

	def __str__(self):
		return self.day_of_week + '_' + str(self.start_time)[:5]	+ '_' + self.class_type.name



