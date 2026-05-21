from django.contrib import admin
from news.models import CustomUser, Publisher, Article, Newsletter

"""
Django admin configuration for the news application.

Registers the CustomUser, Publisher, Article, and Newsletter models
with the Django admin site so they can be managed through the admin interface.
"""


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for the CustomUser model.

    Displays username, email, and role. Allows filtering by role and
    searching by username or email address.
    """
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """
    Admin interface for the Publisher model.

    Displays the publisher name with a search field.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin interface for the Article model.

    Displays title, author, publisher, approval status, and publication date.
    Supports filtering by approval status and publication date, and full-text
    searching by title and content.
    """
    list_display = ('title', 'author', 'publisher', 'approved', 'published_date')
    list_filter = ('approved', 'published_date')
    search_fields = ('title', 'content')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Admin interface for the Newsletter model.

    Displays title, publisher, and publication date.
    Supports filtering by publication date and full-text searching by title
    and content.
    """
    list_display = ('title', 'publisher', 'published_date')
    list_filter = ('published_date',)
    search_fields = ('title', 'content')
