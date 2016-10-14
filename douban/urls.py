from django.conf.urls import url
from . import views

app_name = 'douban'
urlpatterns = [
    url(r'^book/$', views.BookListView.as_view(), name='book_list'),

]