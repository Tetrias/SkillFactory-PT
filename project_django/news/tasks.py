from .models import PostLimiter, Post, Subscribers, Category
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from celery import shared_task
import datetime as dt


@shared_task
def LimitReset():
    """Ежедневная очистка лимита на количество постов."""
    PostLimiter.objects.all().delete()


@shared_task
def WeeklyNewsReport():
    """Еженедельная рассылка новостей пользователям."""
    category_list = Category.objects.all()
    for category in category_list:
        recipient_list = []
        mail_list = Subscribers.objects.all().filter(category=category)
        for user in mail_list:
            recipient_list.append(user)
        today = timezone.now()
        week_ago = today - dt.timedelta(days=7)
        posts_list = Post.objects.filter(time__range=[f"{week_ago}", f"{today}"])
        for recipient in recipient_list:
            html_content = render_to_string(
                'distribution/weekly_report.html',
                {
                    'posts': posts_list,
                    'name': recipient.user.username,
                }
            )

            name = recipient.user.username
            send_mail(
                subject='Еженедельная рассылка новостей.',
                message=f'Здравствуй, {name}. Новая статья в твоём любимом разделе!',
                from_email=None,
                recipient_list=[recipient.user.email],
                fail_silently=False,
                html_message=html_content,
            )


@shared_task
def send_post_notify(**kwargs):
    """Рассылка новостей, в случае если был создан новый пост."""
    category_list = kwargs['category']
    post_id = kwargs['post_id']
    title = kwargs['title']
    text = kwargs['text']
    if len(kwargs['category']) == 1:
        subject = f'"Новая статья в категории "{category_list[0]["name"]}"'
    else:
        subject = 'Новая статья в категориях: '
        count = 0
        for c in category_list:
            subject += c['name']
            count += 1
            if not count == len(category_list):
                subject += ', '
            else:
                subject += '.'

    recipient_list = []
    for category in category_list:
        mail_list = Subscribers.objects.all().filter(pk=category['id'])
        for user in mail_list:
            recipient_list.append(user)
    recipient_list = list(set(recipient_list))

    for recipient in recipient_list:
        html_content = render_to_string(
            'distribution/make_distribution.html',
            {
                'post_path': f'http://127.0.0.1:8000/posts/{post_id}',
                'title': title,
                'text': text,
                'name': recipient.user.username,
            }
        )

        name = recipient.user.username
        send_mail(
            subject=subject,
            message=f'Здравствуй, {name}. Новая статья в твоём любимом разделе!\n' + title,
            from_email=None,
            recipient_list=[recipient.user.email],
            fail_silently=False,
            html_message=html_content,
        )
