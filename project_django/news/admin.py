from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comments


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comments)
