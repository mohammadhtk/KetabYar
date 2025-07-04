from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import BookStatusSerializer
from books.utils.book_service import *
from books.utils.swagger_docs import *


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


@user_book_statuses_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_book_statuses_api(request):
    queryset = get_user_book_statuses(request.user)
    serializer = BookStatusSerializer(queryset, many=True)
    return Response(serializer.data)


@set_book_status_schema
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_book_status_api(request):
    data = request.data
    openlibrary_id = data.get("openlibrary_id")
    status = data.get("status")

    if not openlibrary_id or not status:
        return Response(
            {"detail": "Both 'openlibrary_id' and 'status' are required."},
            status=400
        )

    instance = set_or_update_book_status(request.user, openlibrary_id, status)
    serializer = BookStatusSerializer(instance)
    return Response(serializer.data)

@related_books_schema
@api_view(['GET'])
def get_related_books_view(request, openlibrary_id):
    limit = request.query_params.get("limit", 5)
    books = get_related_books_by_subject(openlibrary_id, limit=int(limit))
    return Response(books)
