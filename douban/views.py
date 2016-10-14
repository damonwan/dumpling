from .models import Book
from django.views.generic.list import ListView

class BookListView(ListView):
    template_name = 'douban/list.html'
    context_object_name = 'book_list'
    model = Book
    paginate_by = 10
