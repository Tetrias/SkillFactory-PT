from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post, Subscribers


@receiver(post_save, sender=Post, dispatch_uid="my_unique_identifier")
def post_notify(sender, instance, created, **kwargs):
    html_content = render_to_string(
        'distribution/make_distribution.html',
        {
            'distribution': instance,
        }
    )

    if created:
        subject = f'В категории пополнение {instance.title}'
    else:
        subject = f'Произошли изменения в {instance.title}'
    recipient_list = []
    for category in instance.category.all():
        mail_list = Subscribers.objects.all().filter(category=category)
        for user in mail_list:
            recipient_list.append(user.user.email)
    recipient_list = list(set(recipient_list))
    print(instance.category.all())
    print(recipient_list)

    send_mail(
        subject=subject,
        message=instance.text,
        from_email=None,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_content,
    )
