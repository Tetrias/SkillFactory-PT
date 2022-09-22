from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Post
from .filters import ProductFilter
from .forms import PostForm


class HomeView(TemplateView):
    """Home page"""
    template_name = 'flatpages/default.html'
    context_object_name = 'main'


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


class NewsCreate(CreateView):
    """Создание новостной статьи."""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        """Метод для изменения значения типа поста, на новостной."""
        post = form.save(commit=False)
        post.type = False
        return super().form_valid(form)


class ArticleCreate(CreateView):
    """Создание статьи."""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostUpdate(UpdateView):
    """Редактирование поста."""
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
    """Удаление поста."""
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
