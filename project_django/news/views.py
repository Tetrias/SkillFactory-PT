from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Post, Author
from .filters import ProductFilter
from .forms import PostForm


class HomeView(TemplateView):
    """Home page"""
    template_name = 'flatpages/default.html'
    context_object_name = 'main'


class IndexView(LoginRequiredMixin, TemplateView):
    """Страница авторизованного пользователя."""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Проверка если пользователь в группе авторов, если в группе, то отображаем его рейтинг."""
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        author = Author.objects.get(user=self.request.user)
        context.update({'rating': author.rating})
        return context


@login_required
def become_author(request):
    """Назначить пользователя автором."""
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')


class PostsList(ListView):
    """Дженерик для отображения всех постов, с ограничением отображения 10 постов на страницу."""
    model = Post
    ordering = '-time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class SearchPosts(ListView):
    """Дженерик для поиска постов, отображение то же, что и у дженерика выше."""
    model = Post
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Метод для фильтрации постов."""
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """Метод для отображения даты создания/редактирования поста."""
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    """Дженерик для отображения конкретного поста."""
    model = Post
    template_name = 'post.html'
    context_object_name = 'posts'


class NewsCreate(PermissionRequiredMixin, CreateView):
    """Создание новостной статьи."""
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        """
        Метод для изменения значения типа поста.
        А так же автоматическое добавление, в поле автора, текущего пользователя.
        """
        post = form.save(commit=False)
        user = self.request.user
        if self.request.path == '/posts/news/create/':
            post.type = False
        post.author = Author.objects.get(user=user)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование поста."""
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    """Удаление поста."""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
