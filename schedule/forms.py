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
        cleaned_data = super(ClassOccurrenceForm, self).clean()
        students = cleaned_data.get('students')
        course = cleaned_data.get('course')
        if students and course:
            if students.count() > course.max_number_of_students:
                raise ValidationError({
                    'students': (
                        f"Maksymalna liczba kursantów wynosi {course.max_number_of_students}. "
                        f"Próbujesz zapisać {students.count()} kursantów."
                    )
                })
        return cleaned_data
