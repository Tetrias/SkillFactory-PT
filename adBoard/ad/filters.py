import django_filters
from django import forms
from .models import Advertisement, Response


class AdsFilter(django_filters.FilterSet):
    """Фильтр для поиска объявлений"""
    text = django_filters.CharFilter(lookup_expr='icontains')

    time = django_filters.DateFilter(
        field_name='time',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Advertisement
        fields = ['title', 'time', 'category']


class ResponseFilter(django_filters.FilterSet):
    """Фильтр для поиска откликов"""
    text = django_filters.CharFilter(lookup_expr='icontains')

    time = django_filters.DateFilter(
        field_name='time',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Response
        fields = ['text', 'time', 'status']
