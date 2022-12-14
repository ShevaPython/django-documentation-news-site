from django.urls import path

from .views import HomeNews, ShowPost, AddNews, NewsByCategory, test, register, user_login,user_logout,email

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ShowPost.as_view(), name='view_news'),
    path('news/add-news', AddNews.as_view(), name='add_news'),
    path('news/test/', test, name='test'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/',user_logout,name='logout'),
    path('contactemail',email,name = 'email')

]
