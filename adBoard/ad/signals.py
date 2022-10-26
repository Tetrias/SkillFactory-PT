from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Advertisement, Response
from .tasks import send_post_notify, send_response_notify, send_response_replay


@receiver(post_save, sender=Advertisement)
def post_notify(sender, instance, **kwargs):
    """Рассылка новостей, в случае изменений в модели объявлений."""
    if not kwargs['created']:
        pass
    else:
        category = [instance.category.name, instance.category.id]
        send_post_notify.delay(
            category=category,
            post_id=instance.id,
            title=instance.title,
            text=instance.text,
        )


@receiver(post_save, sender=Response)
def response_notify(sender, instance, **kwargs):
    ad = Advertisement.objects.get(pk=instance.ad.id)
    if not kwargs['created']:
        author = ad.user
        send_response_notify.delay(
            email=author.email,
            name=author.username,
            id=ad.id,
            title=ad.title,
        )
    else:
        user = instance.user
        send_response_replay.delay(
            email=user.email,
            name=user.username,
            id=ad.id,
            title=ad.title,
        )
