"""
URL patterns for the news application.

This module defines the URL routing for the news app, mapping URLs to
view functions and class-based views for articles, newsletters, and publishers.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('publishers/create/', views.create_publisher, name='create_publisher'),
    path('articles/create/', views.create_article, name='create_article'),
    path('newsletters/create/', views.create_newsletter, name='create_newsletter'),
    path('articles/approve/<int:article_id>/', views.approve_article, name='approve_article'),
    path('api/articles/', views.ArticleListAPI.as_view(), name='api_articles'),
]