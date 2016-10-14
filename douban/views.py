from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Book
from django.utils import timezone

class BookListView(generic.ListView):
    template_name = 'douban/list.html'
    context_object_name = 'book_list'
    def get_queryset(self):
        return Book.objects.order_by('id')[:100]

class BookDetailView(generic.DetailView):
    pass
    
class MovieListView(generic.ListView):
    template_name = 'douban/book/list.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Book.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]