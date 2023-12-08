from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(60)(MainPage.as_view()), name='main'),
    path('news/', cache_page(60*5)(ShowAllNews.as_view()), name='show_all_news'),
    path('articles/', ShowAllArticles.as_view(), name='show_all_articles'),
    path('news/create/', CreateNews.as_view(), name='create_news'),
    path('articles/create/', CreateArticles.as_view(), name='create_articles'),
    path('news/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('news/update/<slug:slug>/', UpdatePost.as_view(), name='update_post'),
    path('news/delete/<slug:slug>/', DeletePost.as_view(), name='delete_post'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    path('get_author/', get_author, name='upgrade'),
    path('category/<slug:category_slug>/', CategoryPostList.as_view(), name='category'),
    path('subscr/<slug:slug>/', subscr, name='subscr'),
]
