from django.urls import path
from .views import AdList, AdDetail, AdSearch, AdCreate, \
    AdUpdate, CategoryDetail, ResponseToAd, subscribe, ResponseDetail, ResponseList, accept_response

urlpatterns = [
    path('', AdList.as_view(), name='ads'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('search/', AdSearch.as_view(), name='ad_search'),
    path('<int:pk>/edit/', AdUpdate.as_view(), name='ad_edit'),
    path('<int:pk>/response/', ResponseToAd.as_view(), name='ad_response'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category_view'),
    path('category/<int:pk>/subscribe/', subscribe, name='category_subscribe'),
    path('category/<int:pk>/unsubscribe/', subscribe, name='category_unsubscribe'),
    path('response/', ResponseList.as_view(), name='response_list'),
    path('response/<int:pk>/', ResponseDetail.as_view(), name='response'),
    path('response/<int:pk>/accept', accept_response, name='accept'),
    path('response/<int:pk>/decline', accept_response, name='decline')
]
