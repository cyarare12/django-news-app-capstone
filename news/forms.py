from django import forms
from .models import Article, Newsletter, Publisher

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content']

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']