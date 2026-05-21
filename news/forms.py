from django import forms
from .models import Article, Newsletter, Publisher

"""
Django forms for the news application.

This module provides ModelForm classes for creating and editing
news-related objects through the web interface.
"""


class ArticleForm(forms.ModelForm):
    """
    Form for creating and editing news articles.

    Fields:
        title (CharField): The headline of the article.
        content (TextField): The body content of the article.
        publisher (ForeignKey): The publisher associated with the article.
    """
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']


class NewsletterForm(forms.ModelForm):
    """
    Form for creating and editing newsletters.

    Fields:
        title (CharField): The newsletter title.
        content (TextField): The newsletter body content.
    """
    class Meta:
        model = Newsletter
        fields = ['title', 'content']


class PublisherForm(forms.ModelForm):
    """
    Form for creating and editing news publishers.

    Fields:
        name (CharField): The name of the publishing organisation.
    """
    class Meta:
        model = Publisher
        fields = ['name']