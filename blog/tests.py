from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import resolve, reverse
import pytz

from .models import Category, Post
from .views import post_detail, post_list, search


class UrlsTest(TestCase):

    def test_posts_url_resolves(self):
        url = reverse('blog:posts')
        self.assertEqual(resolve(url).func, post_list)

    def test_search_url_resolves(self):
        url = reverse('blog:search')
        self.assertEqual(resolve(url).func, search)

    def test_post_url_resolves(self):
        url = reverse('blog:post', args=[1])
        self.assertEqual(resolve(url).func, post_detail)


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        user = User.objects.create_user(username='testuser')

        self.category_1 = Category.objects.create(name='Category 1')
        self.category_2 = Category.objects.create(name='Category 2')

        self.post_1 = Post.objects.create(
            author=user, title='Post in category 1')
        self.post_2 = Post.objects.create(
            author=user, title='Post in category 2', content='test')
        self.post_3 = Post.objects.create(
            author=user, title='Post in category 1 and 2', content='test')
        self.post_1.category.set([self.category_1])
        self.post_2.category.set([self.category_2])
        self.post_3.category.set([self.category_1, self.category_2])

    def test_post_list(self):
        posts_url = reverse('blog:posts')
        response = self.client.get(posts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'core/base.html', '/blog/post_list.html')

    def test_search_by_category(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?cat=category-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set([i for i in response.context['posts']]), set(
            [self.post_1, self.post_3]))
        self.assertTemplateUsed(
            response, 'core/base.html', '/blog/post_list.html')

    def test_search_by_query(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set([i for i in response.context['posts']]), set(
            [self.post_2, self.post_3]))

    def test_search_by_category_and_query(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?q=test&cat=category-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set([i for i in response.context['posts']]), set([self.post_3]))

    def test_no_search_criteria_selected(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?q=&category=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set([i for i in response.context['posts']]), set(
            [self.post_1, self.post_2, self.post_3]))

    def test_order_posts_by_creation_date_from_newest(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?order=n')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([i for i in response.context['posts']], [
                         self.post_3, self.post_2, self.post_1])

    def test_order_posts_by_creation_date_from_oldest(self):
        search_url = reverse('blog:search')
        response = self.client.get(search_url + '?order=o')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([i for i in response.context['posts']], [
                         self.post_1, self.post_2, self.post_3])

    def test_post_detail(self):
        post_url = reverse('blog:post', args=[self.post_1.id])
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'core/base.html', '/blog/post_detail.html')


class CategoryTest(TestCase):

    def setUp(self):
        self.category_1 = Category.objects.create(name='Category name')

    def test_object_name_is_name(self):
        self.assertEqual(str(self.category_1), self.category_1.name)

    def test_slug_is_assigned(self):
        self.assertEqual(self.category_1.slug, 'category-name')

    def test_slug_is_unique(self):
        category_2 = Category.objects.create(name='Category-name')
        self.assertNotEqual(self.category_1.slug, category_2.slug)
        self.assertEqual(category_2.slug, 'category-name-1')


class PostTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123')
        self.timezone = pytz.timezone('Europe/Warsaw')

    def test_was_published(self):
        post_future_publish_date = Post.objects.create(
            author=self.user,
            published=self.timezone.localize(datetime.today() + timedelta(days=1)))
        post_now_publish_date = Post.objects.create(
            author=self.user,
            published=self.timezone.localize(datetime.today()))
        post_past_publish_date = Post.objects.create(
            author=self.user,
            published=self.timezone.localize(datetime.today() - timedelta(days=1)))
        self.assertEqual(post_future_publish_date.was_published(), False)
        self.assertEqual(post_now_publish_date.was_published(), True)
        self.assertEqual(post_past_publish_date.was_published(), True)

    def test_object_name_is_title(self):
        post = Post.objects.create(author=self.user)
        self.assertEqual(str(post), post.title)
