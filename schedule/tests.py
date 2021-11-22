from datetime import date, datetime, time, timedelta
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from .factories import ClassOccurrenceFactory, ClassTypeFactory, CourseFactory, TeacherFactory, UserFactory
from .forms import ClassOccurrenceForm
from .models import ClassOccurrence, Course
from .views import class_occurrence_list, user_class_occurrence_list


class FixedDateTime(datetime):

    @classmethod
    def today(cls):
        return cls(2019, 1, 14)

class FixedDate(date):

    @classmethod
    def today(cls):
        return cls(2019, 1, 14)

class UrlsTest(TestCase):

    def test_week_view_url_resolves(self):
        url = reverse('schedule:week_view')
        self.assertEqual(resolve(url).func, class_occurrence_list)

    def test_user_class_list_url_resolves(self):
        url = reverse('schedule:user_class_list')
        self.assertEqual(resolve(url).func, user_class_occurrence_list)


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username='username',
                               password=make_password('password'))
        class_type_0 = ClassTypeFactory(name='class type 0')
        class_type_1 = ClassTypeFactory(name='class type 1')
        course_0 = CourseFactory(
            class_type=class_type_0, weekday=Course.DAYS_OF_WEEK[0][0], start_time=time(hour=8))
        course_1 = CourseFactory(
            class_type=class_type_0, weekday=Course.DAYS_OF_WEEK[0][0], start_time=time(hour=9))
        course_2 = CourseFactory(
            class_type=class_type_1, weekday=Course.DAYS_OF_WEEK[0][0], start_time=time(hour=10))
        dates = [(datetime(2019, 1, 7) + timedelta(days=i * 7)).date()
                 for i in range(5)]
        # Creates ClassOccurrence objects. 3 classes for 5 weeks starting
        # 2019-01-07
        for course in [course_0, course_1, course_2]:
            for d in dates:
                ClassOccurrenceFactory(course=course, date=d)

    def setUp(self):
        self.client = Client()

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_initial_view(self):
        '''Initial view for current week should show 3 classes'''
        response = self.client.get(reverse('schedule:week_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 3)

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_for_past_weeks_not_available(self):
        '''The view for past weeks should return message schedule is not available'''
        response = self.client.get(
            reverse('schedule:week_view') + '?day=2019-01-07')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 0)
        self.assertEqual(
            response.context[-1]['messages']['week_view'], 'Grafik niedostępny')

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_next_week_available(self):
        '''The view for the next week should show 3 classes'''
        response = self.client.get(
            reverse('schedule:week_view') + '?day=2019-01-21')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 3)

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_3rd_week_from_today_available(self):
        '''The view for the week after next week should show 3 classes'''
        response = self.client.get(
            reverse('schedule:week_view') + '?day=2019-01-28')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 3)

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_4th_week_from_today_not_available(self):
        '''The view for 4th week from current week, should return message "schedule is not available"'''
        response = self.client.get(
            reverse('schedule:week_view') + '?day=2019-02-04')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 0)
        self.assertEqual(
            response.context[-1]['messages']['week_view'], 'Grafik niedostępny')

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_schedule_no_classes(self):
        '''The view schould show the message "Brak zaplanowanych zajęć"'''
        with patch('schedule.views.datetime') as mock_datetime:
            mock_datetime.today.return_value = datetime(2019, 3, 1, 12, 0, 0)
            mock_datetime.side_effect = lambda *args, **kw: datetime(
                *args, **kw)
            response = self.client.get(reverse('schedule:week_view'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                len(response.context[-1]['classes_during_week']), 0)
            self.assertEqual(
                response.context[-1]['messages']['week_view'], 'Brak zaplanowanych zajęć')

    @patch('schedule.views.datetime', FixedDateTime)
    def test_week_view_search_class_type(self):
        '''The view should show 2 classes "class type 0"'''
        response = self.client.get(
            reverse('schedule:week_view') + '?day=2019-01-14&class-type=class-type-0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context[-1]['classes_during_week']), 2)

    def test_week_view_user_can_sign_up_for_class(self):
        '''User can sign up for class and confirming message is returned'''
        class_ = ClassOccurrence.objects.all().first()
        self.assertFalse(self.user in class_.students.all())
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('schedule:week_view'),
                                    {'class-id': class_.pk, 'action': 'sign-up', 'modal': 'True'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(class_.students.count(), 1)
        self.assertTrue(self.user in class_.students.all())
        self.assertEqual(
            response.context[-1]['messages']['modal'], 'Zostałeś zapisany')

    def test_week_view_user_can_sign_off_from_class(self):
        '''User can sign off from class and confirming message is returned'''
        class_ = ClassOccurrence.objects.all().first()
        class_.students.add(self.user)
        self.assertEqual(class_.students.count(), 1)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('schedule:week_view'),
                                    {'class-id': class_.pk, 'action': 'sign-off', 'modal': 'True'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(class_.students.count(), 0)
        self.assertEqual(
            response.context[-1]['messages']['modal'], 'Zostałeś wypisany')

    @patch('schedule.views.date', FixedDate)
    def test_user_class_list_initial_view_returns_200_status_and_correct_context(self):
        '''Check response status and context that is used to display search options on the page'''
        class_occurrence_2017 = ClassOccurrenceFactory(
            date=datetime(2017, 1, 2))
        class_occurrence_2017.students.add(self.user)
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('schedule:user_class_list'))
        months = {'styczeń': '1', 'luty': '2', 'marzec': '3', 'kwiecień': '4',
                  'maj': '5', 'czerwiec': '6', 'lipiec': '7', 'sierpień': '8',
                  'wrzesień': '9', 'październik': '10', 'listopad': '11', 'grudzień': '12'}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['months'], months)
        self.assertEqual(response.context[-1]
                         ['years'], ['2019', '2018', '2017'])

    def test_user_class_list_view_returns_user_classes(self):
        class_occurrence = ClassOccurrenceFactory(date=datetime(2017, 1, 2))
        class_occurrence.students.add(self.user)
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('schedule:user_class_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('2017-01-02_09:00_class type',
                      str(response.context[-1]['user_classes'][0]))

    def test_user_class_list_search_by_year_and_month(self):
        class_occurrence_2017_01 = ClassOccurrenceFactory(
            date=datetime(2017, 1, 2))
        class_occurrence_2017_05 = ClassOccurrenceFactory(
            date=datetime(2017, 7, 5))
        class_occurrence_2017_01.students.add(self.user)
        class_occurrence_2017_05.students.add(self.user)
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('schedule:user_class_list'), {
                                   'year': '2017', 'month': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['year'], '2017')
        self.assertEqual(response.context[-1]['month'], '1')
        self.assertEqual(len(response.context[-1]['user_classes']), 1)
        self.assertIn('2017-01-02_09:00_class type',
                      str(response.context[-1]['user_classes'][0]))

    def test_user_class_list_redirect_anonymous_user_to_login_page(self):
        response = self.client.get(reverse('schedule:user_class_list'))
        self.assertEqual(response.status_code, 302)

    def test_user_class_list_view_returns_message_when_user_have_no_classes(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('schedule:user_class_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context[-1]['messages']['class_list'], "Nie masz jeszcze żadnych zajęć.")
        self.assertFalse(response.context[-1]['user_classes'])

    def test_user_class_list_user_can_sign_off_from_class(self):
        '''The user should sign-off from the class'''
        class_ = ClassOccurrence.objects.all().first()
        class_.students.add(self.user)
        self.assertEqual(class_.students.count(), 1)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('schedule:user_class_list'), {
                                    'class-id': class_.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(class_.students.count(), 0)
        self.assertEqual(
            response.context[-1]['messages']['sign_off'], "Zostałeś wypisany")
        self.assertFalse(response.context[-1]['user_classes'])


class ClassTypeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.class_type_0 = ClassTypeFactory(name="class type")
        cls.class_type_1 = ClassTypeFactory(name="class-type")

    def test_name_label(self):
        field_option = self.class_type_0._meta.get_field('name').verbose_name
        self.assertEqual(field_option, 'nazwa zajęć')

    def test_name_max_length(self):
        field_option = self.class_type_0._meta.get_field('name').max_length
        self.assertEqual(field_option, 50)

    def test_name_unique(self):
        field_option = self.class_type_0._meta.get_field('name').unique
        self.assertTrue(field_option, 'Unique has to be set to True')

    def test_slug_label(self):
        field_option = self.class_type_0._meta.get_field('slug').verbose_name
        self.assertEqual(field_option, 'slug')

    def test_description_label(self):
        field_option = self.class_type_0._meta.get_field(
            'description').verbose_name
        self.assertEqual(field_option, 'opis zajęć')

    def test_description_null(self):
        field_option = self.class_type_0._meta.get_field('description').null
        self.assertTrue(field_option)

    def test_description_blank(self):
        field_option = self.class_type_0._meta.get_field('description').blank
        self.assertTrue(field_option)

    def test_color_label(self):
        field_option = self.class_type_0._meta.get_field('color').verbose_name
        self.assertEqual(field_option, 'kolor')

    def test_created_label(self):
        field_option = self.class_type_0._meta.get_field(
            'created').verbose_name
        self.assertEqual(field_option, 'data utworzenia')

    def test_created_auto_now_add_is_true(self):
        field_option = self.class_type_0._meta.get_field(
            'created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_label(self):
        field_option = self.class_type_0._meta.get_field(
            'updated').verbose_name
        self.assertEqual(field_option, 'data aktualizacji')

    def test_updated_auto_now_is_true(self):
        field_option = self.class_type_0._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_str_reprezentation_is_name(self):
        self.assertEqual(str(self.class_type_0), self.class_type_0.name)

    def test_getting_unique_slug(self):
        self.assertEqual(self.class_type_0.slug, 'class-type')
        self.assertEqual(self.class_type_1.slug, 'class-type-1')


class TeacherTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.teacher_0 = TeacherFactory()

    def test_name_label(self):
        field_option = self.teacher_0._meta.get_field('name').verbose_name
        self.assertEqual(field_option, 'imię i nazwisko instruktora')

    def test_name_max_length(self):
        field_option = self.teacher_0._meta.get_field('name').max_length
        self.assertEqual(field_option, 50)

    def test_description_label(self):
        field_option = self.teacher_0._meta.get_field(
            'description').verbose_name
        self.assertEqual(field_option, 'opis instruktora')

    def test_created_label(self):
        field_option = self.teacher_0._meta.get_field('created').verbose_name
        self.assertEqual(field_option, 'data utworzenia')

    def test_created_auto_now_add_is_true(self):
        field_option = self.teacher_0._meta.get_field('created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_label(self):
        field_option = self.teacher_0._meta.get_field('updated').verbose_name
        self.assertEqual(field_option, 'data aktualizacji')

    def test_updated_auto_now_is_true(self):
        field_option = self.teacher_0._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_str_reprezentation_is_name(self):
        self.assertEqual(str(self.teacher_0), self.teacher_0.name)


class CourseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.class_type_0 = ClassTypeFactory()
        cls.teacher_0 = TeacherFactory()
        cls.course_0 = CourseFactory()

    def test_class_type_label(self):
        field_option = self.course_0._meta.get_field('class_type').verbose_name
        self.assertEqual(field_option, 'rodzaj zajęć')

    def test_name_label(self):
        field_option = self.course_0._meta.get_field('name').verbose_name
        self.assertEqual(field_option, 'nazwa kursu')

    def test_name_max_length(self):
        field_option = self.course_0._meta.get_field('name').max_length
        self.assertEqual(field_option, 300)

    def test_name_null_true(self):
        field_option = self.course_0._meta.get_field('name').null
        self.assertTrue(field_option)

    def test_name_blank_true(self):
        field_option = self.course_0._meta.get_field('name').blank
        self.assertTrue(field_option)

    def test_teacher_label(self):
        field_option = self.course_0._meta.get_field('teacher').verbose_name
        self.assertEqual(field_option, 'instruktor prowadzący')

    def test_weekday_label(self):
        field_option = self.course_0._meta.get_field('weekday').verbose_name
        self.assertEqual(field_option, 'dzień tygodnia')

    def test_weekday_max_length(self):
        field_option = self.course_0._meta.get_field('weekday').max_length
        self.assertEqual(field_option, 14)

    def test_start_time_label(self):
        field_option = self.course_0._meta.get_field('start_time').verbose_name
        self.assertEqual(field_option, 'godzina rozpoczęcia')

    def test_end_time_label(self):
        field_option = self.course_0._meta.get_field('end_time').verbose_name
        self.assertEqual(field_option, 'godzina zakończenia')

    def test_end_time_blank_true(self):
        field_option = self.course_0._meta.get_field('end_time').blank
        self.assertTrue(field_option)

    def test_duration_label(self):
        field_option = self.course_0._meta.get_field('duration').verbose_name
        self.assertEqual(field_option, 'czas trwania zajęć [min]')

    def test_duration_default(self):
        field_option = self.course_0._meta.get_field('duration').default
        self.assertEqual(field_option, 55)

    def test_active_label(self):
        field_option = self.course_0._meta.get_field('active').verbose_name
        self.assertEqual(field_option, 'aktywny')

    def test_active_default(self):
        field_option = self.course_0._meta.get_field('active').default
        self.assertTrue(field_option)

    def test_note_label(self):
        field_option = self.course_0._meta.get_field('note').verbose_name
        self.assertEqual(field_option, 'uwagi')

    def test_note_max_length(self):
        field_option = self.course_0._meta.get_field('note').max_length
        self.assertEqual(field_option, 300)

    def test_note_null(self):
        field_option = self.course_0._meta.get_field('note').null
        self.assertTrue(field_option)

    def test_note_blank(self):
        field_option = self.course_0._meta.get_field('note').blank
        self.assertTrue(field_option)

    def test_max_number_of_students_label(self):
        field_option = self.course_0._meta.get_field(
            'max_number_of_students').verbose_name
        self.assertEqual(field_option, 'maksymalna liczba uczestników')

    def test_max_number_of_students_dafault(self):
        field_option = self.course_0._meta.get_field(
            'max_number_of_students').default
        self.assertEqual(field_option, 30)

    def test_created_label(self):
        field_option = self.course_0._meta.get_field('created').verbose_name
        self.assertEqual(field_option, 'data utworzenia')

    def test_created_auto_now_add_is_true(self):
        field_option = self.course_0._meta.get_field('created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_label(self):
        field_option = self.course_0._meta.get_field('updated').verbose_name
        self.assertEqual(field_option, 'data aktualizacji')

    def test_updated_auto_now_is_true(self):
        field_option = self.course_0._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_weekday_start_time_class_name(self):
        object_name = (self.course_0.weekday + '_'
                       + str(self.course_0.start_time)[:5] + '_'
                       + self.course_0.class_type.name)
        self.assertEqual(str(self.course_0), object_name)

    def test_clean_course_course_start_and_finish_same_day(self):
        '''Check if class ends the same day'''
        course_1 = CourseFactory.build(
            teacher=self.teacher_0, class_type=self.class_type_0,
            start_time=time(hour=23, minute=30), duration=60)
        self.assertRaises(ValidationError, course_1.full_clean)
        try:
            course_1.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'start_time':
                                              ["Zajęcia muszą zaczynać i kończyć się tego samego dnia"]})


class ClassOccurrenceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.teacher_0 = TeacherFactory()
        cls.teacher_1 = TeacherFactory()

        cls.future_date = (timezone.now() + timedelta(days=7)).date()
        cls.today_date = timezone.now().date()
        cls.past_date = (timezone.now() - timedelta(days=7)).date()
        cls.weekday_0 = Course.DAYS_OF_WEEK[cls.today_date.weekday()][0]

    def setUp(self):
        self.course_0 = CourseFactory(teacher=self.teacher_0, weekday=self.weekday_0,
                                      start_time=time(hour=9))

        self.class_occurrence_0 = ClassOccurrenceFactory(course=self.course_0,
                                                         date=self.future_date)

    def test_course_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'course').verbose_name
        self.assertEqual(field_option, 'nazwa kursu')

    def test_date_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'date').verbose_name
        self.assertEqual(field_option, 'data')

    def test_date_help_text(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'date').help_text
        self.assertEqual(field_option,
                         'Data musi być w przyszłości i przypadać na dzień tygodnia, w którym odbywa się kurs')

    def test_start_time_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'start_time').verbose_name
        self.assertEqual(field_option, 'godzina rozpoczęcia')

    def test_start_time_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'start_time').blank
        self.assertTrue(field_option)

    def test_end_time_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'end_time').verbose_name
        self.assertEqual(field_option, 'godzina zakończenia')

    def test_end_time_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'end_time').blank
        self.assertTrue(field_option)

    def test_main_teacher_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'main_teacher').verbose_name
        self.assertEqual(field_option, 'instruktor')

    def test_main_teacher_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'main_teacher').blank
        self.assertTrue(field_option)

    def test_main_teacher_null_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'main_teacher').null
        self.assertTrue(field_option)

    def test_substitute_teacher_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'substitute_teacher').verbose_name
        self.assertEqual(field_option, 'zastępstwo')

    def test_substitute_teacher_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'substitute_teacher').blank
        self.assertTrue(field_option)

    def test_substitute_teacher_null_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'substitute_teacher').null
        self.assertTrue(field_option)

    def test_students_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'students').verbose_name
        self.assertEqual(field_option, 'uczestnicy')

    def test_students_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'students').blank
        self.assertTrue(field_option)

    def test_cancelled_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'cancelled').verbose_name
        self.assertEqual(field_option, 'anulowane')

    def test_cancelled_default(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'cancelled').default
        self.assertFalse(field_option, 'By default class is not cancelled')

    def test_note_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'note').verbose_name
        self.assertEqual(field_option, 'uwagi')

    def test_note_max_length(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'note').max_length
        self.assertEqual(field_option, 300)

    def test_note_blank_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field('note').blank
        self.assertTrue(field_option)

    def test_note_null_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field('note').null
        self.assertTrue(field_option)

    def test_created_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'created').verbose_name
        self.assertEqual(field_option, 'data utworzenia')

    def test_created_auto_now_add_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_label(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'updated').verbose_name
        self.assertEqual(field_option, 'data aktualizacji')

    def test_updated_auto_now_is_true(self):
        field_option = self.class_occurrence_0._meta.get_field(
            'updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_date_start_time_course_name(self):
        object_name = (str(self.class_occurrence_0.date) + '_' + str(self.class_occurrence_0.start_time)[:5]
                       + '_' + self.class_occurrence_0.course.name)
        self.assertEqual(str(self.class_occurrence_0), object_name)

    def test_save_saves_start_time(self):
        '''If no start_time saves the value of start_time from related course object'''
        self.assertEqual(self.class_occurrence_0.start_time.isoformat(
            timespec='minutes'), '09:00')

    def test_save_saves_end_time(self):
        '''If no end_time saves the value of end_time from related course object'''
        self.assertEqual(self.class_occurrence_0.end_time.isoformat(
            timespec='minutes'), '09:55')

    def test_save_saves_main_teacher(self):
        '''If no main_teacher saves the value of teacher from related course object'''
        self.assertEqual(self.class_occurrence_0.main_teacher,
                         self.course_0.teacher)

    def test_save_does_not_save_start_and_end_time_if_start_time_exists(self):
        '''start_time and end_time should not be overwritten should not be overwritten'''
        class_occurrence_1 = ClassOccurrenceFactory(course=self.course_0, date=self.future_date,
                                                    start_time=time(hour=19), end_time=time(hour=20))
        self.assertEqual(class_occurrence_1.start_time.isoformat(
            timespec='minutes'), '19:00')
        self.assertEqual(class_occurrence_1.end_time.isoformat(
            timespec='minutes'), '20:00')

    def test_save_does_not_save_main_teacher_if_it_exists(self):
        '''main_teacher in class occurrence should not be overwritten'''
        class_occurrence_1 = ClassOccurrenceFactory(
            course=self.course_0, date=self.future_date, main_teacher=self.teacher_1)
        self.assertEqual(class_occurrence_1.main_teacher, self.teacher_1)

    def test_property_teacher_is_main_teacher(self):
        '''If substitute teacher is not defined, teacher is same as main_teacher'''
        self.assertEqual(self.class_occurrence_0.teacher, self.teacher_0)

    def test_property_teacher_is_substitute_teacher(self):
        '''If substitute teacher is defined, teacher is same as substitute_teacher'''
        self.class_occurrence_0.substitute_teacher = self.teacher_1
        self.class_occurrence_0.save()
        self.assertEqual(self.class_occurrence_0.main_teacher, self.teacher_0)
        self.assertEqual(self.class_occurrence_0.teacher, self.teacher_1)

    def test_property_number_of_students(self):
        users = UserFactory.create_batch(3)
        self.class_occurrence_0.students.add(*users)
        self.assertEqual(self.class_occurrence_0.number_of_students, 3)

    def test_property_number_of_places_left(self):
        self.course_0.max_number_of_students = 5
        self.course_0.save()
        users = UserFactory.create_batch(3)
        self.class_occurrence_0.students.add(*users)
        self.assertEqual(self.class_occurrence_0.number_of_places_left, 2)

    def test_property_assign_status_for_cancelled_classes(self):
        '''Should assign status 'Anulowane' to cancelled classes'''
        self.class_occurrence_0.cancelled = True
        self.class_occurrence_0.save()
        self.assertEqual(self.class_occurrence_0.status, 'Anulowane')

    def test_property_assign_status_for_future_classes(self):
        '''Should assign status 'Planowane' to classes in the future'''
        self.class_occurrence_1 = ClassOccurrenceFactory(course=self.course_0,
                                                         date=self.future_date)
        self.assertEqual(self.class_occurrence_1.status, 'Planowane')

    def test_property_assign_status_for_current_classes(self):
        '''
            Should assign status:
            "Trwają" to class that is just starting and finishing,
            "Zakończone" to the class that finished 1 min ago,
            "Planowane" to the class that starts in one minut
        '''
        with patch('schedule.models.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2019, 1, 1, 12, 0, 0)
            mock_datetime.combine.side_effect = lambda *args, **kw: datetime.combine(
                *args, **kw)

            course_class_just_finished = CourseFactory(
                start_time=time(10, 59), duration=60)
            class_occurrence_class_just_finished = ClassOccurrenceFactory(
                course=course_class_just_finished, date=date(2019, 1, 1))

            course_class_ends = CourseFactory(
                start_time=time(11, 0), duration=60)
            class_occurrence_class_ends = ClassOccurrenceFactory(
                course=course_class_ends, date=date(2019, 1, 1))

            course_class_starts = CourseFactory(
                start_time=time(12, 0), duration=60)
            class_occurrence_class_starts = ClassOccurrenceFactory(
                course=course_class_starts, date=date(2019, 1, 1))

            course_class_almost_starts = CourseFactory(
                start_time=time(12, 1), duration=60)
            class_occurrence_class_almost_starts = ClassOccurrenceFactory(
                course=course_class_almost_starts, date=date(2019, 1, 1))

            self.assertEqual(
                class_occurrence_class_just_finished.status, 'Zakończone')
            self.assertEqual(
                class_occurrence_class_ends.status, 'Trwają')
            self.assertEqual(
                class_occurrence_class_starts.status, 'Trwają')
            self.assertEqual(
                class_occurrence_class_almost_starts.status, 'Planowane')

    def test_property_assign_status_for_past_classes(self):
        '''Should assign status "Zakończone" to classes in the past'''
        self.class_occurrence_1 = ClassOccurrenceFactory(course=self.course_0,
                                                         date=self.past_date)
        self.assertEqual(self.class_occurrence_1.status, 'Zakończone')

    def test_clean_class_is_same_weekday_as_course(self):
        '''The date has to fall on the weekday when course takes place'''
        date_not_corresponding_to_weekday = (
            timezone.now() + timedelta(days=1)).date()
        course_1 = CourseFactory(
            teacher=self.teacher_0, weekday=self.weekday_0, start_time=time(hour=10))
        class_occurrence_1 = ClassOccurrenceFactory.build(
            course=course_1, date=date_not_corresponding_to_weekday)
        self.assertRaises(ValidationError, class_occurrence_1.full_clean)
        try:
            class_occurrence_1.full_clean()
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'date': [f"Te zajęcia odbywają się w: {course_1.weekday[2:]}. Wybierz inną datę."]})

    def test_clean_class_with_past_date_can_not_be_created_or_updated(self):
        '''User can't create or update class occurrence when it's time is in the past'''
        course_1 = CourseFactory(
            teacher=self.teacher_0, weekday=self.weekday_0, start_time=time(hour=10))
        class_occurrence_1 = ClassOccurrenceFactory.build(
            course=course_1, date=self.past_date)
        self.assertRaises(ValidationError, class_occurrence_1.full_clean)
        try:
            class_occurrence_1.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'__all__':
                                              ["Czas zajęć nie może być w przeszłości."]})

    def test_clean_classes_can_not_occur_at_the_same_time(self):
        '''Two classes can't occur at the same time'''
        course_1 = CourseFactory(
            teacher=self.teacher_0, weekday=self.weekday_0, start_time=time(hour=9, minute=30))
        class_occurrence_1 = ClassOccurrenceFactory.build(
            course=course_1, date=self.future_date)
        self.assertRaises(ValidationError, class_occurrence_1.full_clean)
        try:
            class_occurrence_1.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'__all__':
                                              [f"Czas trwania zajęć koliduje z zajęciami {self.course_0.name}"]})

    def test_clean_substitute_teacher_is_not_main_teacher(self):
        '''Substitute teacher can't be same as main teacher'''
        course_1 = CourseFactory(
            teacher=self.teacher_0, weekday=self.weekday_0, start_time=time(hour=10))
        class_occurrence_1 = ClassOccurrenceFactory.build(course=course_1,
                                                          date=self.future_date, substitute_teacher=self.teacher_0)
        self.assertRaises(ValidationError, class_occurrence_1.full_clean)
        try:
            class_occurrence_1.full_clean()
        except ValidationError as e:
            self.assertEqual(e.message_dict, {'substitute_teacher':
                                              ["Zastępstwo nie może się odbywać z instruktorem prowadzącym kurs."]})

    def test_clean_number_of_students_smaller_than_max_students_number(self):
        '''Check if number of students is not bigger than maximum number'''
        self.course_0.max_number_of_students = 5
        self.course_0.save()
        users = UserFactory.create_batch(10)
        form = ClassOccurrenceForm(
            {'students': [*users], 'course': self.course_0.pk}, instance=self.class_occurrence_0)
        self.assertEqual(form.errors,
                         {'students': ["Maksymalna liczba kursantów wynosi 5. Próbujesz zapisać 10 kursantów."]})
