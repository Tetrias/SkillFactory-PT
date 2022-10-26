from .models import Advertisement, Subscribers, Category
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from celery import shared_task
import datetime as dt


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
        posts_list = Advertisement.objects.filter(time__range=[f"{week_ago}", f"{today}"])
        for recipient in recipient_list:
            name = recipient.user.username
            html_content = render_to_string(
                'distribution/weekly_report.html',
                {
                    'posts': posts_list,
                    'name': name,
                    'category': category.name
                }
            )

            send_mail(
                subject='Еженедельная рассылка новостей.',
                message=f'Здравствуй, {name}. Список объявлений вышедшие в категории {category.name} за эту неделю.',
                from_email=None,
                recipient_list=[recipient.user.email],
                fail_silently=False,
                html_message=html_content,
            )


@shared_task
def send_post_notify(**kwargs):
    """Рассылка новостей, в случае если было создано новое объявление."""
    category = kwargs['category']
    post_id = kwargs['post_id']
    title = kwargs['title']
    text = kwargs['text']
    subject = f'Новое объявление в категории: {category[0]}'

    recipient_list = []
    mail_list = Subscribers.objects.all().filter(category=category[1])
    for user in mail_list:
        recipient_list.append(user)

    for recipient in recipient_list:
        name = recipient.user.username
        html_content = render_to_string(
            'distribution/make_distribution.html',
            {
                'post_path': f'http://127.0.0.1:8000/ads/{post_id}',
                'title': title,
                'text': text,
                'name': name,
                'category': category[0]
            }
        )

        send_mail(
            subject=subject,
            message=f'Здравствуй, {name}. Новая статья в твоём любимом разделе!\n' + title,
            from_email=None,
            recipient_list=[recipient.user.email],
            fail_silently=False,
            html_message=html_content,
        )


@shared_task
def send_response_notify(**kwargs):
    html_content = render_to_string(
        'distribution/response.html',
        {
            'response_path': f'http://127.0.0.1:8000/ads/response/{kwargs["id"]}',
            'title': kwargs["title"],
            'name': kwargs["name"],
        }
    )

    send_mail(
        subject='Вы получили отклик на объявление',
        message=f'Здравствуй, {kwargs["name"]}. На ваше объявление появился новый отклик:\n' + kwargs["title"],
        from_email=None,
        recipient_list=[kwargs["email"]],
        fail_silently=False,
        html_message=html_content,
    )


@shared_task
def send_response_replay(**kwargs):

    html_content = render_to_string(
        'distribution/response_replay.html',
        {
            'response_path': f'http://127.0.0.1:8000/ads/response/{kwargs["id"]}',
            'title': kwargs["title"],
            'name': kwargs["name"],
        }
    )

    send_mail(
        subject='Вы получили ответ на ваш отклик',
        message=f'Здравствуй, {kwargs["name"]}. Ваш отклик на объявление {kwargs["title"]} был принят!',
        from_email=None,
        recipient_list=[kwargs["email"]],
        fail_silently=False,
        html_message=html_content,
    )
