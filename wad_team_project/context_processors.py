from booklists.models import Book, Author
def add_top_books(request):
    books = list(Book.objects.order_by('average_rating').filter().all().reverse()[:5])
    return {
        'top_5_books' : books,
    }
