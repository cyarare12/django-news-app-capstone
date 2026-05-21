from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import requests
from news.models import Article

@receiver(post_save, sender=Article)
def article_approved(sender, instance, created, **kwargs):
    """
    Signal handler for when an article is approved.
    Sends email to subscribers and posts to X (Twitter).
    """
    if instance.approved and not created:  # Only on update to approved
        # Send emails to subscribers
        subscribers = set()
        if instance.publisher:
            subscribers.update(instance.publisher.subscribers.all())
        subscribers.update(instance.author.subscribed_journalists.all())
        emails = [user.email for user in subscribers if user.email]
        if emails:
            send_mail(
                f'New Article Approved: {instance.title}',
                f'Content: {instance.content}\n\nAuthor: {instance.author.username}',
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )

        # Post to X (Twitter)
        # Placeholder: Replace with actual API call
        # Requires Twitter API keys
        # tweet_text = f'New article: {instance.title} by {instance.author.username}'
        # response = requests.post(
        #     'https://api.twitter.com/2/tweets',
        #     headers={'Authorization': f'Bearer {settings.TWITTER_BEARER_TOKEN}'},
        #     json={'text': tweet_text}
        # )
        print(f"Would post to Twitter: New article: {instance.title}")  # Placeholder