from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    """Модель для автора статьи."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        """Метод для обновлений рейтинга автора."""
        comments = Comments.objects.filter(user_id=self.user).aggregate(Sum('rating'))
        post_rating = Post.objects.filter(author_id=self.id).aggregate(Sum('rating'))
        posts = Post.objects.filter(author_id=self.id).values('id')
        comments_post_rating = 0
        for i in range(len(posts)):
            comments_posts = Comments.objects.filter(post_id=posts[i]['id']).values('rating')
            for y in range(len(comments_posts)):
                comments_post_rating += comments_posts[y]['rating']
        self.rating = comments['rating__sum'] + comments_post_rating + post_rating['rating__sum'] * 3
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель для постов."""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        """Метод для отображения превью текста поста, ограничение в 124 символа."""
        prev = self.text[:124]
        return prev

    def like(self):
        """Метод для повышения рейтинга поста."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Метод для понижения рейтинга поста."""
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.preview()}'

    def get_absolute_url(self):
        """Метод для открытия страницы созданного поста, после его создания."""
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        """В случае изменений в модели, очищаем старый кэш."""
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class PostCategory(models.Model):
    """Модель для связи "многие ко многим" между категориями и постами."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    """Модель для комментариев от пользователей."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        """Метод для повышения рейтинга комментария."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Метод для понижения рейтинга комментария."""
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.user.username.title()}: {self.comment.title()}'


class Subscribers(models.Model):
    """Модель для связи "многие ко многим", между пользователем и категориями, для рассылки новостей."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostLimiter(models.Model):
    """Модель для подсчета количества постов созданных пользователем."""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
