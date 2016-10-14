from .models import Book
from django.views.generic.list import ListView
from django.db.models import Q

class BookListView(ListView):
    template_name = 'douban/list.html'
    context_object_name = 'book_list'
    model = Book
    paginate_by = 20
    
    def get_queryset(self):
        book_list = Book.objects.order_by('-rating_numbers').all()
        keyword = self.request.GET.get('keyword')
        if keyword:
            book_list = book_list.filter(Q(name__contains=keyword)|Q(info__contains=keyword)|Q(tags__contains=keyword))
        rating = self.request.GET.get('rating')
        if rating:
            book_list = book_list.filter(rating__gte=rating)
        ratingnumbers = self.request.GET.get('ratingnumbers')
        if ratingnumbers:
            book_list = book_list.filter(rating_numbers__gte=ratingnumbers)
        return book_list
    
#     def get_context_data(self, **kwargs):
#         context = super(BookListView,self).get_context_data(**kwargs)
#         taglist = Book.objects.values('tags').annotate()
#         context['taglist'] = taglist
#         return context