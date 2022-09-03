from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .forms import NewsForm
from .models import News, Category


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 2

    # extra_context = {'title':'Главная страница'} метод для статических файлов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_publish=True).select_related('category')


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список с Базы даных',
#
#     }
#     return render(request, 'news/index.html', context=context)

class NewsByCategory(ListView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_publish=True).select_related('category')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news,
#
#                'category': category
#
#                }
#     return render(request, 'news/category.html', context=context)

class ShowPost(DeleteView):
    model = News
    template_name = 'news/view_news.html'
    # pk_url_kwarg = 'news_id'
    context_object_name = 'item'


# def view_news(request, news_id):
#     item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'item': item})


class AddNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # raise_exception = True


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save()
#             return redirect('home')
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

def test(request):
    news = News.objects.all()
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)
    return render(request, 'news/test.html', {'page_obj': page_objects})
