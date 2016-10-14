from django.conf.urls import url
from . import views

app_name = 'douban'
urlpatterns = [
    url(r'^book/$', views.BookListView.as_view(), name='book_list'),
    url(r'^book/(?P<pk>[0-9]+)/$', views.BookDetailView.as_view(), name='detail'),
    
    url(r'^movie/$', views.MovieListView.as_view(), name='movie_list'),

]