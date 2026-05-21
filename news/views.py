from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Article, Newsletter, Publisher
from .serializers import ArticleSerializer
from .forms import ArticleForm, NewsletterForm, PublisherForm

@login_required
@permission_required('news.view_article', raise_exception=True)
def article_list(request):
    """
    Display list of articles based on user role.

    Editors see unapproved articles, others see approved articles.
    """
    if request.user.role == 'editor':
        articles = Article.objects.filter(approved=False)
    else:
        articles = Article.objects.filter(approved=True)
    return render(request, 'news/article_list.html', {'articles': articles})

@login_required
@permission_required('news.add_article', raise_exception=True)
def create_article(request):
    """
    Handle article creation by journalists.
    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'news/create_article.html', {'form': form})

@login_required
def create_publisher(request):
    """
    Handle publisher creation.
    """
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            # Optionally, add creator as editor or journalist
            if request.user.role in ['editor', 'journalist']:
                if request.user.role == 'editor':
                    publisher.editors.add(request.user)
                else:
                    publisher.journalists.add(request.user)
            return redirect('article_list')
    else:
        form = PublisherForm()
    return render(request, 'news/create_publisher.html', {'form': form})

@login_required
@permission_required('news.add_newsletter', raise_exception=True)
def create_newsletter(request):
    """
    Handle newsletter creation by journalists.
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.publisher = request.user
            newsletter.save()
            return redirect('article_list')  # Or a newsletter list
    else:
        form = NewsletterForm()
    return render(request, 'news/create_newsletter.html', {'form': form})

@login_required
@permission_required('news.change_article', raise_exception=True)
def approve_article(request, article_id):
    """
    Handle article approval by editors.

    Approves the article.
    """
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.approved = True
        article.save()  # Signals will handle email and Twitter posting
        return redirect('article_list')
    return render(request, 'news/approve_article.html', {'article': article})

class ArticleListAPI(generics.ListAPIView):
    """
    API view for retrieving articles based on user subscriptions.

    Returns approved articles from subscribed publishers and journalists.
    """
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'reader':
            publishers = user.subscribed_publishers.all()
            journalists = user.subscribed_journalists.all()
            return Article.objects.filter(
                approved=True
            ).filter(
                models.Q(publisher__in=publishers) | models.Q(author__in=journalists)
            )
        return Article.objects.none()
