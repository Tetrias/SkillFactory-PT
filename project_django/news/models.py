from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
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


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        prev = self.text[:124]
        return prev

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.preview()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
