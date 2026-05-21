from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import CustomUser, Publisher, Article, Newsletter

class ArticleAPITestCase(APITestCase):
    """
    Test cases for the Article API endpoints.
    """

    def setUp(self):
        """
        Set up test data for API tests.
        """
        self.reader = CustomUser.objects.create_user(username='reader', password='pass', role='reader', email='reader@example.com')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.journalist = CustomUser.objects.create_user(username='journalist', password='pass', role='journalist', email='journalist@example.com')
        self.article = Article.objects.create(title='Test Article', content='Content', author=self.journalist, publisher=self.publisher, approved=True)
        self.reader.subscribed_publishers.add(self.publisher)

    def test_get_articles_for_subscribed_reader(self):
        """
        Test that authenticated readers get articles from subscribed publishers.
        """
        self.client.login(username='reader', password='pass')
        response = self.client.get(reverse('api_articles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Article')

    def test_get_articles_for_subscribed_journalist(self):
        """
        Test that readers get articles from subscribed journalists.
        """
        self.reader.subscribed_journalists.add(self.journalist)
        self.client.login(username='reader', password='pass')
        response = self.client.get(reverse('api_articles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_access_denied(self):
        """
        Test that unauthenticated users cannot access the API.
        """
        response = self.client.get(reverse('api_articles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_approved_articles_returned(self):
        """
        Test that only approved articles are returned.
        """
        Article.objects.create(title='Unapproved', content='Content', author=self.journalist, publisher=self.publisher, approved=False)
        self.client.login(username='reader', password='pass')
        response = self.client.get(reverse('api_articles'))
        self.assertEqual(len(response.data), 1)  # Only the approved one

class ModelTestCase(TestCase):
    """
    Test cases for models.
    """

    @classmethod
    def setUpTestData(cls):
        # Create groups
        article_ct = ContentType.objects.get_for_model(Article)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)
        view_article = Permission.objects.get(content_type=article_ct, codename='view_article')
        add_article = Permission.objects.get(content_type=article_ct, codename='add_article')
        change_article = Permission.objects.get(content_type=article_ct, codename='change_article')
        delete_article = Permission.objects.get(content_type=article_ct, codename='delete_article')
        view_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='view_newsletter')
        add_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='add_newsletter')
        change_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='change_newsletter')
        delete_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='delete_newsletter')

        reader_group, _ = Group.objects.get_or_create(name='Reader')
        reader_group.permissions.set([view_article, view_newsletter])

        editor_group, _ = Group.objects.get_or_create(name='Editor')
        editor_group.permissions.set([view_article, change_article, delete_article, view_newsletter, change_newsletter, delete_newsletter])

        journalist_group, _ = Group.objects.get_or_create(name='Journalist')
        journalist_group.permissions.set([add_article, view_article, change_article, delete_article, add_newsletter, view_newsletter, change_newsletter, delete_newsletter])

    def test_custom_user_creation(self):
        """
        Test creating a custom user.
        """
        user = CustomUser.objects.create_user(username='testuser', password='pass', role='reader')
        self.assertEqual(user.role, 'reader')
        self.assertIn(user, Group.objects.get(name='Reader').user_set.all())

    def test_publisher_creation(self):
        """
        Test creating a publisher.
        """
        publisher = Publisher.objects.create(name='Test Pub')
        self.assertEqual(str(publisher), 'Test Pub')

    def test_article_creation(self):
        """
        Test creating an article.
        """
        user = CustomUser.objects.create_user(username='author', password='pass', role='journalist')
        article = Article.objects.create(title='Title', content='Content', author=user, approved=True)
        self.assertEqual(str(article), 'Title')

    def test_newsletter_creation(self):
        """
        Test creating a newsletter.
        """
        user = CustomUser.objects.create_user(username='publisher', password='pass', role='journalist')
        newsletter = Newsletter.objects.create(title='Newsletter', content='Content', publisher=user)
        self.assertEqual(str(newsletter), 'Newsletter')
