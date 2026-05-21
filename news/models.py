from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.urls import reverse

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser with role-based functionality.

    Attributes:
        role (str): User's role - 'reader', 'editor', or 'journalist'
        subscribed_publishers (ManyToMany): Publishers the user is subscribed to (for readers)
        subscribed_journalists (ManyToMany): Journalists the user is subscribed to (for readers)
        independent_articles (ManyToMany): Articles published independently (for journalists)
        independent_newsletters (ManyToMany): Newsletters published independently (for journalists)
    """
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('journalist', 'Journalist'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    # For readers
    subscribed_publishers = models.ManyToManyField('Publisher', blank=True, related_name='subscribers')
    subscribed_journalists = models.ManyToManyField('self', blank=True, related_name='journalist_subscribers', symmetrical=False)

    # For journalists
    independent_articles = models.ManyToManyField('Article', blank=True, related_name='independent_authors')
    independent_newsletters = models.ManyToManyField('Newsletter', blank=True, related_name='independent_publishers')

    def save(self, *args, **kwargs):
        """
        Override save method to assign user to appropriate group and clear role-specific fields.

        Assigns user to group based on role and clears fields not applicable to the role.
        """
        super().save(*args, **kwargs)
        group_name = self.role.capitalize()
        try:
            group = Group.objects.get(name=group_name)
            self.groups.set([group])
        except Group.DoesNotExist:
            pass  # Group not created yet, or error
        if self.role == 'journalist':
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()
        elif self.role == 'reader':
            self.independent_articles.clear()
            self.independent_newsletters.clear()

class Publisher(models.Model):
    """
    Model representing a news publisher.

    Attributes:
        name (str): Name of the publisher
        editors (ManyToMany): Editors associated with this publisher
        journalists (ManyToMany): Journalists associated with this publisher
    """
    name = models.CharField(max_length=100)
    editors = models.ManyToManyField(CustomUser, related_name='publisher_editors', limit_choices_to={'role': 'editor'})
    journalists = models.ManyToManyField(CustomUser, related_name='publisher_journalists', limit_choices_to={'role': 'journalist'})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('article_list')

class Article(models.Model):
    """
    Model representing a news article.

    Attributes:
        title (str): Article title
        content (str): Article content
        author (ForeignKey): Author of the article
        publisher (ForeignKey): Publisher (optional for independent articles)
        approved (bool): Whether the article is approved for publication
        published_date (datetime): Date the article was published
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True)
    approved = models.BooleanField(default=False)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_list')

class Newsletter(models.Model):
    """
    Model representing a newsletter.

    Attributes:
        title (str): Newsletter title
        content (str): Newsletter content
        publisher (ForeignKey): User who published the newsletter
        published_date (datetime): Date the newsletter was published
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    publisher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='newsletters')
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_list')
