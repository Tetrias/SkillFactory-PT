import django_filters
from .models import Post, Category
from django import forms
from django.utils.translation import gettext as _


class CustomBooleanWidget(django_filters.widgets.BooleanWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = (("", _("Любое")), ("true", _("Статья")), ("false", _("Новость")))


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Category',
        conjoined=True,
    )
    article = django_filters.BooleanFilter(widget=CustomBooleanWidget)
    title = django_filters.CharFilter(lookup_expr='icontains')

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
        model = Post
        fields = ['title', 'time', 'category', 'article']
