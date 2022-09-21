from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'category', ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        if text is None:
            raise ValidationError({"text": "Содержание не может быть пустым."})
        title = cleaned_data.get("title")

        if title is None:
            raise ValidationError({"title": "Название не может быть пустым."})

        return cleaned_data
