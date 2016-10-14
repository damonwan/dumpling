from django.conf.urls import url
from . import views

app_name = 'douban'
urlpatterns = [
    url(r'^book/$', views.BookListView.as_view(), name='book_list'),
    url(r'^movie/$', views.MovieListView.as_view(), name='movie_list'),
    
    url(r'^book/spider$', views.book_spider),
    url(r'^movie/spider$', views.movie_spider),
]