from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import News, Category


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешно авторизованы')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


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


class ShowPost(DeleteView):
    model = News
    template_name = 'news/view_news.html'
    # pk_url_kwarg = 'news_id'
    context_object_name = 'item'


class AddNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # raise_exception = True


def test(request):
    news = News.objects.all()
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)
    return render(request, 'news/test.html', {'page_obj': page_objects})


def email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'welcome-my@ukr.net',
                             ['shevadotka@gmail.com'], fail_silently=True,)
            if mail:
                messages.success(request, 'Письмо отправленно')
                return redirect('email')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = ContactForm()
    return render(request, 'news/contactemail.html', {'form': form})
