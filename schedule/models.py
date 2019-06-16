from django.db import models
from colorful.fields import RGBColorField
from about.models import Teacher as TeacherDescription
from classes.models import ClassOffer as ClassDescription
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class ClassType(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Nazwa zajęć')
    slug = models.SlugField(unique=True)
    description = models.ForeignKey(
        ClassDescription, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Opis zajęć')
    color = RGBColorField(default='#007bff', verbose_name='Kolor')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Data aktualizacji')

    class Meta:
        verbose_name = 'Rodzaj zajęć'
        verbose_name_plural = 'Rodzaje zajęć'

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while ClassType.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug or self.name not in self.slug:
            self.slug = self._get_unique_slug()
        super(ClassType, self).save(*args, **kwargs)


class Teacher(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='Imię i nazwisko instruktora')
    description = models.OneToOneField(
        TeacherDescription, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Opis instruktora')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Data aktualizacji')

    class Meta:
        verbose_name = 'Instruktor'
        verbose_name_plural = 'Instruktorzy'

    def __str__(self):
        return self.name


class Course(models.Model):
    class_type = models.ForeignKey(
        ClassType, on_delete=models.CASCADE, verbose_name='rodzaj zajęć')
    name = models.CharField(max_length=300, null=True,
                            blank=True, verbose_name='nazwa kursu')
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name='instruktor prowadzący')

    MONDAY = "1_Poniedziałek"
    TUESDAY = "2_Wtorek"
    WEDNESDAY = "3_Środa"
    THURSDAY = "4_Czwartek"
    FRIDAY = "5_Piątek"
    SATURDAY = "6_Sobota"
    SUNDAY = "7_Niedziela"

    DAYS_OF_WEEK = (
        (MONDAY, "Poniedziałek"),
        (TUESDAY, "Wtorek"),
        (WEDNESDAY, "Środa"),
        (THURSDAY, "Czwartek"),
        (FRIDAY, "Piątek"),
        (SATURDAY, "Sobota"),
        (SUNDAY, "Niedziela"),
    )
    weekday = models.CharField(
        max_length=14, choices=DAYS_OF_WEEK, verbose_name='dzień tygodnia')
    start_time = models.TimeField(verbose_name='godzina rozpoczęcia')
    end_time = models.TimeField(blank=True, verbose_name='godzina zakończenia')
    duration = models.PositiveSmallIntegerField(
        default=55, verbose_name='czas trwania zajęć [min]')
    active = models.BooleanField(default=True, verbose_name='aktywny')
    note = models.CharField(max_length=300, null=True,
                            blank=True, verbose_name='uwagi')
    max_number_of_students = models.PositiveSmallIntegerField(
        default=30, verbose_name='Maksymalna liczba uczestników')

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'kurs'
        verbose_name_plural = 'kursy'
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return self.weekday + '_' + str(self.start_time)[:5] + '_' + self.class_type.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.class_type.name
        self.end_time = (datetime.combine(
            date.today(), self.start_time) + timedelta(minutes=self.duration)).time()
        super(Course, self).save(*args, **kwargs)


class ClassOccurrence(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='nazwa kursu')
    date = models.DateField(
        verbose_name='data', help_text="Data musi być w przyszłości i przypadać na dzień tygodnia, w którym odbywa się kurs")
    start_time = models.TimeField(
        blank=True, verbose_name='godzina rozpoczęcia')
    end_time = models.TimeField(blank=True, verbose_name='godzina zakończenia')
    main_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True,
                                     blank=True, related_name='main_teacher_set', verbose_name='instruktor')
    substitute_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True,
                                           blank=True, related_name='substitute_teacher_set', verbose_name='zastępstwo')
    students = models.ManyToManyField(
        User, blank=True, verbose_name='uczestnicy')
    cancelled = models.BooleanField(default=False, verbose_name='anulowane')
    note = models.CharField(max_length=300, null=True,
                            blank=True, verbose_name='uwagi')

    created = models.DateTimeField(
        auto_now_add=True, verbose_name='data utworzenia')
    updated = models.DateTimeField(
        auto_now=True, verbose_name='data aktualizacji')

    class Meta:
        verbose_name = 'Zaplanowane zajęcia'
        verbose_name_plural = 'Zaplanowane zajęcia'
        ordering = ['date', models.F('course').asc()]

    def __str__(self):
        return str(self.date) + '_' + str(self.start_time)[:5] + '_' + self.course.name

    @property
    def teacher(self):
        if self.substitute_teacher:
            return self.substitute_teacher
        return self.course.teacher

    @property
    def number_of_students(self):
        return self.students.count()
    number_of_students.fget.short_description = 'zapisanych'

    @property
    def number_of_places_left(self):
        return self.course.max_number_of_students - self.students.count()
    number_of_places_left.fget.short_description = 'wolne'

    @property
    def status(self):
        if self.cancelled:
            return 'Anulowane'
        else:
            start_datetime = datetime.combine(
                self.date, self.course.start_time)
            end_datetime = datetime.combine(self.date, self.course.end_time)
            now = datetime.now()
            if now < start_datetime:
                return 'Planowane'
            elif start_datetime <= now <= end_datetime:
                return 'Trwają'
            elif end_datetime < now:
                return 'Zakończone'
    status.fget.short_description = 'status'

    def clean(self, *args, **kwargs):
        super(ClassOccurrence, self).clean(*args, **kwargs)
        # Date has to correspond to the weekday in course instance
        if self.date.isoweekday() != int(self.course.weekday[0]):
            raise ValidationError({'date': (f"Te zajęcia odbywają się w: {self.course.weekday[2:]}. Wybierz inną datę.")})
        # Checks if date and time is not in the past
        if datetime.combine(self.date, self.course.start_time) < datetime.now():
            raise ValidationError("Czas zajęć nie może być w przeszłości.")
        # Checks if no time collision with other classes on the same day
        class_same_day = ClassOccurrence.objects.filter(
            date=self.date).exclude(pk=self.pk)
        start = self.course.start_time
        end = self.course.end_time
        for c in class_same_day:
            if (c.start_time <= start < c.end_time or
                    c.start_time < end <= c.end_time or
                    start <= c.start_time and c.end_time <= end):
                raise ValidationError(f"Czas trwania zajęć koliduje z zajęciami {c.course.name}")
        # Substituting teacher has to be different than the teacher in course
        # instance
        if self.substitute_teacher == self.course.teacher:
            raise ValidationError({'substitute_teacher': (
                "Zastępstwo nie może się odbywać z instruktorem prowadzącym kurs.")})

    def save(self, *args, **kwargs):
        if not self.start_time or not self.end_time or not self.main_teacher:
            self.start_time = self.course.start_time
            self.end_time = self.course.end_time
            self.main_teacher = self.course.teacher
        super(ClassOccurrence, self).save(*args, **kwargs)
