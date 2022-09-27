from django_cron import CronJobBase, Schedule
from .models import PostLimiter, Post, Subscribers, Category
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
import datetime as dt


class LimitReset(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'news.limit_reset'

    def do(self):
        PostLimiter.objects.all().delete()


class WeeklyNewsReport(CronJobBase):
    RUN_EVERY_MINS = 10080
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'news.weekly_news_report'

    def do(self):
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
