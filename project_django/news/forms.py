from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    """Форма постов, для редактирования и создания."""
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', ]

    def clean(self):
        """Проверка на то, что заполнение формы было верным"""
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is None:
            raise ValidationError({"text": "Содержание не может быть пустым."})
        title = cleaned_data.get("title")

        if title is None:
            raise ValidationError({"title": "Название не может быть пустым."})

        return cleaned_data


class BasicSignupForm(SignupForm):
    """Автоматически добавляем нового пользователя в группу 'common'"""
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
