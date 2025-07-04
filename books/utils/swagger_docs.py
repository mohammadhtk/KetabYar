from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

limit_param = openapi.Parameter(
    'limit',
    in_=openapi.IN_QUERY,
    description="Maximum number of books to return",
    type=openapi.TYPE_INTEGER,
    required=False
)

search_query_param = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['q'],
    properties={
        'q': openapi.Schema(type=openapi.TYPE_STRING, description='Search query'),
    },
)

category_param = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['category'],
    properties={
        'category': openapi.Schema(type=openapi.TYPE_STRING, description='OpenLibrary category path, e.g., "/subjects/science_fiction"'),
    },
)


books_home_schema = swagger_auto_schema(
    method='get',
    manual_parameters=[limit_param],
    operation_summary="Get books for home page"
)

search_books_schema = swagger_auto_schema(
    method='post',
    operation_summary="Search books",
    request_body=search_query_param,
    responses={200: openapi.Response(description="Books found")},
)

book_detail_schema = swagger_auto_schema(
    method='get',
    operation_summary="Get book detail",
    responses={
        200: openapi.Response(description="Book detail"),
        404: openapi.Response(description="Book not found")
    }
)

all_categories_schema = swagger_auto_schema(
    method='get',
    operation_summary="Get all categories"
)

fetch_category_books_schema = swagger_auto_schema(
    method='post',
    operation_summary="Fetch books by category",
    request_body=category_param,
    responses={
        200: openapi.Response(description="Books retrieved successfully"),
        400: openapi.Response(description="Category link is required"),
    }
)


popular_books_schema = swagger_auto_schema(
    operation_summary="Get popular books",
    manual_parameters=[
        openapi.Parameter(
            'limit',
            openapi.IN_QUERY,
            description="Number of books to return",
            type=openapi.TYPE_INTEGER,
            required=False,
            default=10
        )
    ]
)


# Related books
related_books_schema = swagger_auto_schema(
    method='get',
    operation_summary="Get related books by OpenLibrary ID",
    manual_parameters=[
        openapi.Parameter(
            'openlibrary_id',
            openapi.IN_PATH,
            description="OpenLibrary work ID",
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={200: openapi.Response(description="Related books list")}
)

# User book statuses
user_book_statuses_schema = swagger_auto_schema(
    method='get',
    operation_summary="Get saved/in-progress/finished books of user",
    responses={200: openapi.Response(description="List of user book statuses")}
)

set_book_status_schema = swagger_auto_schema(
    method='post',
    operation_summary="Set or update a book status for user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['openlibrary_id', 'status'],
        properties={
            'openlibrary_id': openapi.Schema(type=openapi.TYPE_STRING, description='OpenLibrary work ID'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['saved', 'in_progress', 'finished'])
        }
    ),
    responses={200: openapi.Response(description="Book status updated")}
)
