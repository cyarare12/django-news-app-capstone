from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Article, Newsletter

class Command(BaseCommand):
    """
    Management command to set up user groups and permissions for the news application.
    """
    help = 'Set up groups and permissions for the news app'

    def handle(self, *args, **options):
        """
        Execute the command to create/update groups and assign permissions.
        """
        # Get content types
        article_ct = ContentType.objects.get_for_model(Article)
        newsletter_ct = ContentType.objects.get_for_model(Newsletter)

        # Get permissions
        view_article = Permission.objects.get(content_type=article_ct, codename='view_article')
        add_article = Permission.objects.get(content_type=article_ct, codename='add_article')
        change_article = Permission.objects.get(content_type=article_ct, codename='change_article')
        delete_article = Permission.objects.get(content_type=article_ct, codename='delete_article')

        view_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='view_newsletter')
        add_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='add_newsletter')
        change_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='change_newsletter')
        delete_newsletter = Permission.objects.get(content_type=newsletter_ct, codename='delete_newsletter')

        # Reader group
        reader_group, created = Group.objects.get_or_create(name='Reader')
        reader_group.permissions.set([view_article, view_newsletter])
        if created:
            self.stdout.write('Created Reader group')
        else:
            self.stdout.write('Updated Reader group')

        # Editor group
        editor_group, created = Group.objects.get_or_create(name='Editor')
        editor_group.permissions.set([view_article, change_article, delete_article, view_newsletter, change_newsletter, delete_newsletter])
        if created:
            self.stdout.write('Created Editor group')
        else:
            self.stdout.write('Updated Editor group')

        # Journalist group
        journalist_group, created = Group.objects.get_or_create(name='Journalist')
        journalist_group.permissions.set([add_article, view_article, change_article, delete_article, add_newsletter, view_newsletter, change_newsletter, delete_newsletter])
        if created:
            self.stdout.write('Created Journalist group')
        else:
            self.stdout.write('Updated Journalist group')

        self.stdout.write('Groups and permissions set up successfully.')