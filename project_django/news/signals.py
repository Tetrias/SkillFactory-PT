from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import PostCategory, Subscribers


@receiver(m2m_changed, sender=PostCategory, dispatch_uid="my_unique_identifier")
def post_notify(sender, instance, **kwargs):
    """Рассылка новостей, в случае если был создан новый пост."""
    if kwargs['action'] == 'pre_add':
        pass
    else:
        category_list = instance.category.all()
        if len(category_list) == 1:
            subject = f'Новая статья в категории "{category_list[0].name}"'
        else:
            subject = 'Новая статья в категориях: '
            count = 0
            for c in category_list:
                subject += c.name
                count += 1
                if not count == len(category_list):
                    subject += ', '
                else:
                    subject += '.'

        recipient_list = []
        for category in category_list:
            mail_list = Subscribers.objects.all().filter(category=category)
            for user in mail_list:
                recipient_list.append(user)
        recipient_list = list(set(recipient_list))
        post_id = instance.id

        for recipient in recipient_list:
            html_content = render_to_string(
                'distribution/make_distribution.html',
                {
                    'post_path': f'http://127.0.0.1:8000/posts/{post_id}',
                    'distribution': instance,
                    'name': recipient.user.username,
                }
            )

            name = recipient.user.username
            send_mail(
                subject=subject,
                message=f'Здравствуй, {name}. Новая статья в твоём любимом разделе!\n' + instance.title,
                from_email=None,
                recipient_list=[recipient.user.email],
                fail_silently=False,
                html_message=html_content,
            )
