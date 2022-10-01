from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from .models import PostCategory
from .tasks import send_post_notify


@receiver(m2m_changed, sender=PostCategory, dispatch_uid="my_unique_identifier")
def post_notify(sender, instance, **kwargs):
    """Рассылка новостей, в случае если был создан новый пост."""
    if kwargs['action'] == 'pre_add':
        pass
    else:
        category = instance.category.all().values('id', 'name')
        send_post_notify.delay(
            category=list(category),
            post_id=instance.id,
            title=instance.title,
            text=instance.text,
        )
