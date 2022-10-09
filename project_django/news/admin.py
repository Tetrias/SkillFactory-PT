from django.contrib import admin
from .models import Category, Author, Post, Comments, Subscribers


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'time', 'author')
    list_filter = ('time', 'category')
    search_fields = ('title', 'category__name', 'author__user__username')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username', 'rating')


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('category', )
    search_fields = ('user__username', )


class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'time', 'rating')
    list_filter = ('time', )
    search_fields = ('user__username', 'post__title')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments, CommentaryAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
