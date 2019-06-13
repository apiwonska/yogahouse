from django import forms
from django.core.exceptions import ValidationError
from .models import ClassOccurrence


class ClassOccurrenceForm(forms.ModelForm):

    class Meta:
        model = ClassOccurrence
        fields = ('students', 'course')

    def clean(self):
        # Checks if number of students inscribed is not greater than allowed
        # for the course
        students = self.cleaned_data.get('students')
        course = self.cleaned_data.get('course')
        if students and course:
            if students.count() > course.max_number_of_students:
                raise ValidationError((f"Maksymalna liczba kursantów wynosi {course.max_number_of_students}. "
                	f"Próbujesz zapisać {students.count()} kursantów."))
        return self.cleaned_data
