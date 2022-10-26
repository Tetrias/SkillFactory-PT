from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Category, Advertisement, Subscribers, Response
from .forms import AdForm, ResponseForm
from .filters import AdsFilter, ResponseFilter


@login_required
def subscribe(request, **kwargs):
    """Метод для подписки на категорию."""
    user = request.user
    category = Category.objects.get(pk=kwargs['pk'])
    if 'unsubscribe' in request.path.split('/'):
        Subscribers.objects.filter(user=user, category=category).delete()
    else:
        Subscribers.objects.create(user=user, category=category)
    return redirect(f"/ads/category/{kwargs['pk']}/")


@login_required
def accept_response(request, **kwargs):
    user = request.user
    response = Response.objects.get(pk=kwargs['pk'])
    print(response.status)
    if user == response.ad.user:
        if 'decline' in request.path.split('/'):
            response.delete()
        else:
            response.status = True
            response.save()
    return redirect(f"/ads/response/")


class HomeView(TemplateView):
    """Home page"""
    template_name = 'default.html'
    context_object_name = 'main'


class AccountView(LoginRequiredMixin, TemplateView):
    """Страница авторизованного пользователя."""
    template_name = 'account/account.html'


class AdList(ListView):
    """Все объявления."""
    model = Advertisement
    ordering = '-time'
    template_name = 'ad/ads.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdSearch(ListView):
    """Поиск объявлений"""
    model = Advertisement
    ordering = '-time'
    template_name = 'ad/ad_search.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        """Метод для фильтрации объявлений."""
        queryset = super().get_queryset()
        self.filterset = AdsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Метод для отображения даты создания/редактирования объявления."""
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class AdDetail(DetailView):
    """Отображение конкретного объявления."""
    model = Advertisement
    template_name = 'ad/ad.html'
    context_object_name = 'ad'


class AdCreate(LoginRequiredMixin, CreateView):
    """Создание объявления."""
    form_class = AdForm
    model = Advertisement
    template_name = 'ad/ad_edit.html'

    def form_valid(self, form):
        """
        Автоматическое добавление, в поле автора, текущего пользователя.
        """
        ad = form.save(commit=False)
        ad.user = self.request.user
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    """Редактирование объявления."""
    form_class = AdForm
    model = Advertisement
    template_name = 'ad/ad_edit.html'

    def form_valid(self, form):
        """Только создатель объявления может редактировать его."""
        ad = form.save(commit=False)
        if self.request.user == ad.user:
            return super().form_valid(form)
        else:
            return redirect(f"/ads/{ad.id}/")


class CategoryDetail(DetailView):
    """Отображение страницы категории."""
    model = Category
    template_name = 'ad/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        """Метод для работы с подписками на категории."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = context['category']
        context['subscribed'] = Subscribers.objects.filter(user=user, category=category).exists()
        return context


class ResponseToAd(LoginRequiredMixin, CreateView):
    """Отклик на объявление."""
    form_class = ResponseForm
    model = Advertisement
    template_name = 'ad/ad_response.html'

    def form_valid(self, form):
        """Привязка объявления к отклику."""
        response = form.save(commit=False)
        path = self.request.path
        user = self.request.user
        ad_id = int((path.replace('/ads/', '')).replace('/response/', ''))
        ad = Advertisement.objects.get(pk=ad_id)
        response.ad = ad
        response.user = user
        return super().form_valid(form)


class ResponseDetail(DetailView):
    """Отображение конкретного отклика."""
    model = Response
    template_name = 'ad/ad_response_detail.html'
    context_object_name = 'response'


class ResponseList(LoginRequiredMixin, ListView):
    """Поиск объявлений"""
    model = Response
    ordering = '-time'
    template_name = 'ad/ad_response_llist.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        """Метод для фильтрации откликов."""
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Метод для отображения даты создания отклика."""
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
