from django.contrib import admin
from news.models import CustomUser, Publisher, Article, Newsletter

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'approved', 'published_date')
    list_filter = ('approved', 'published_date')
    search_fields = ('title', 'content')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'published_date')
    list_filter = ('published_date',)
    search_fields = ('title', 'content')
