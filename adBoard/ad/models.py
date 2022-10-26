from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = RichTextField()
    time = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title.title()}'

    def get_absolute_url(self):
        """Метод для открытия страницы созданного объявления."""
        return reverse('ad_detail', args=[str(self.id)])


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)
    ad = models.OneToOneField(Advertisement, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Метод для открытия страницы созданного объявления."""
        return reverse('ad_detail', args=[str(self.ad.id)])


class Subscribers(models.Model):
    """Модель для связи "многие ко многим", между пользователем и категориями, для рассылки новостей."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
