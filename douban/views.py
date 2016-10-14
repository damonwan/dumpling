from .models import Book, Movie
from django.views.generic.list import ListView
from django.db.models import Q
from douban.spider import spider_book, spider_movie
from django.http.response import JsonResponse

class BookListView(ListView):
    template_name = 'douban/list.html'
    context_object_name = 'item_list'
    model = Book
    paginate_by = 20
    
    def get_queryset(self):
        book_list = Book.objects.order_by('-rating', '-rating_numbers').all().filter(rating__gte=7.5).filter(rating_numbers__gte=10000)
        keyword = self.request.GET.get('keyword')
        if keyword:
            book_list = book_list.filter(Q(name__contains=keyword)|Q(info__contains=keyword)|Q(tags__contains=keyword))
        return book_list
    
class MovieListView(ListView):
    template_name = 'douban/list.html'
    context_object_name = 'item_list'
    model = Movie
    paginate_by = 20
    
    def get_queryset(self):
        movie_list = Movie.objects.order_by('-rating', '-rating_numbers').all().filter(rating__gte=7.5).filter(rating_numbers__gte=10000)
        keyword = self.request.GET.get('keyword')
        if keyword:
            movie_list = movie_list.filter(Q(name__contains=keyword)|Q(info__contains=keyword)|Q(tags__contains=keyword))
        return movie_list

def book_spider(request):
    spider_book.run()
    return JsonResponse('ok', safe=False)
    
def movie_spider(request):
    spider_movie.run()
    return JsonResponse('ok', safe=False)
    
    
    
    
    
    