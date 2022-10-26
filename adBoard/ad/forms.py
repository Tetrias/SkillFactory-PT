from django import forms
from .models import Advertisement, Response


class AdForm(forms.ModelForm):
    """Форма объявлений, для редактирования и создания."""
    class Meta:
        model = Advertisement
        fields = ['title', 'text', 'category', ]


class ResponseForm(forms.ModelForm):
    """Форма для отклика."""
    class Meta:
        model = Response
        fields = ['text']
