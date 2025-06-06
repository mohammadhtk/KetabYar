from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from books.utils.book_service import fetch_home_books, search_books_service, get_book_detail, get_all_categories, fetch_books_by_category, fetch_popular_books
from books.utils.swagger_docs import (
    books_home_schema,
    search_books_schema,
    book_detail_schema,
    all_categories_schema,
    fetch_category_books_schema,
    popular_books_schema
)


@books_home_schema
@api_view(['GET'])
def books_home(request):
    limit = int(request.GET.get("limit", 10))
    books = fetch_home_books(limit)
    return Response({
        "ok": True,
        "message": "Got books successfully!",
        "data": books
    })


@search_books_schema
@api_view(['POST'])
def search_books(request):
    query = request.data.get("q", "")
    books = search_books_service(query)
    return Response({
        "ok": True,
        "message": "Got books successfully!",
        "data": books
    })


@book_detail_schema
@api_view(['GET'])
def book_detail(request, book_link):
    data = get_book_detail(book_link)
    if not data:
        return Response({"ok": False, "message": "Book not found."}, status=404)

    return Response({
        "ok": True,
        "message": "Got book successfully!",
        "data": data
    })

@all_categories_schema
@api_view(['GET'])
def all_categories(request):
    return Response({
        "ok": True,
        "message": "Got categories successfully!",
        "data": get_all_categories()
    })


@fetch_category_books_schema
@api_view(['POST'])
def fetch_category_books(request):
    category_link = request.data.get("category")
    if not category_link:
        return Response({"ok": False, "message": "Category link is required."}, status=400)

    books = fetch_books_by_category(category_link)
    return Response({
        "ok": True,
        "message": "Got books successfully!",
        "data": books
    })


class PopularBooksView(APIView):
    
    @popular_books_schema
    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        books = fetch_popular_books(limit)
        return Response({
            'ok':True,
            'message':"Got popular books successfully!",
            'data': books
        })