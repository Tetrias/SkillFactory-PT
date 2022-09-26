from django.urls import path
from .views import PostsList, PostDetail, SearchPosts, NewsCreate, PostUpdate, PostDelete, CategoryDetail, subscribe


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPosts.as_view(), name='post_search'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', NewsCreate.as_view(), name='article_create'),
   path('category/<int:pk>/', CategoryDetail.as_view(), name='category_view'),
   path('category/<int:pk>/subscribe/', subscribe, name='category_subscribe'),
   path('category/<int:pk>/unsubscribe/', subscribe, name='category_unsubscribe')
]
