from django.urls import path

from .views import HomeNews, ShowPost, AddNews, NewsByCategory, test

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ShowPost.as_view(), name='view_news'),
    path('news/add-news', AddNews.as_view(), name='add_news'),
    path('news/test',test,name='test')

]
