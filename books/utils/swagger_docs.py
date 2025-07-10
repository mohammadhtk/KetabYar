from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

# Parameters
limit_param = OpenApiParameter(
    name='limit',
    location=OpenApiParameter.QUERY,
    description="Maximum number of books to return",
    required=False,
    type=OpenApiTypes.INT
)

book_link_param = OpenApiParameter(
    name='bookLink',
    location=OpenApiParameter.PATH,
    description="OpenLibrary book link (e.g. /books/OL7353617M)",
    required=True,
    type=OpenApiTypes.STR
)

page_param = OpenApiParameter(
    name='page',
    location=OpenApiParameter.QUERY,
    description="Page number",
    required=False,
    type=OpenApiTypes.INT,
    default=1
)

page_size_param = OpenApiParameter(
    name='page_size',
    location=OpenApiParameter.QUERY,
    description="Page size",
    required=False,
    type=OpenApiTypes.INT,
    default=5
)

# ------------------- SCHEMAS -------------------

books_home_schema = extend_schema(
    summary="Get books for home page",
    parameters=[limit_param],
    responses={200: OpenApiResponse(description="Books list")}
)

search_books_schema = extend_schema(
    summary="Search books",
    request={
        "application/json": {
            "type": "object",
            "required": ["q"],
            "properties": {
                "q": {"type": "string", "description": "Search query"}
            }
        }
    },
    responses={200: OpenApiResponse(description="Books found")}
)

book_detail_schema = extend_schema(
    summary="Get book detail",
    responses={
        200: OpenApiResponse(description="Book detail"),
        404: OpenApiResponse(description="Book not found"),
    }
)

all_categories_schema = extend_schema(
    summary="Get all categories",
    responses={200: OpenApiResponse(description="Category list")}
)

fetch_category_books_schema = extend_schema(
    summary="Fetch books by category",
    request={
        "application/json": {
            "type": "object",
            "required": ["category"],
            "properties": {
                "category": {"type": "string", "description": "e.g., '/subjects/science_fiction'"}
            }
        }
    },
    responses={
        200: OpenApiResponse(description="Books retrieved successfully"),
        400: OpenApiResponse(description="Invalid category input")
    }
)

popular_books_schema = extend_schema(
    summary="Get popular books",
    parameters=[limit_param],
    responses={200: OpenApiResponse(description="Popular books list")}
)

related_books_schema = extend_schema(
    summary="Get related books by OpenLibrary book link",
    responses={200: OpenApiResponse(description="Related books list")}
)

user_book_statuses_schema = extend_schema(
    summary="Get saved/in-progress/finished books of user",
    responses={200: OpenApiResponse(description="User book statuses")}
)

set_book_status_schema = extend_schema(
    summary="Set or update a book status for user",
    request={
        "application/json": {
            "type": "object",
            "required": ["openlibrary_id", "status"],
            "properties": {
                "openlibrary_id": {"type": "string", "description": "OpenLibrary work ID"},
                "status": {"type": "string", "enum": ["saved", "in_progress", "finished"]}
            }
        }
    },
    responses={200: OpenApiResponse(description="Book status updated")}
)

genre_recommendations_schema = extend_schema(
    summary="Recommend books by user's favorite genres",
    responses={200: OpenApiResponse(description="Genre recommendations")}
)

history_recommendations_schema = extend_schema(
    summary="Recommend books based on user's reading history",
    responses={200: OpenApiResponse(description="History-based recommendations")}
)

prompt_recommendations_schema = extend_schema(
    summary="Ask Gemini to recommend books for custom user question",
    request={
        "application/json": {
            "type": "object",
            "required": ["prompt"],
            "properties": {
                "prompt": {"type": "string", "description": "User's custom question or input"}
            }
        }
    },
    responses={200: OpenApiResponse(description="AI book recommendations")}
)

chat_history_schema = extend_schema(
    summary="List chat history with Gemini",
    parameters=[page_param, page_size_param],
    responses={200: OpenApiResponse(description="Chat history list")}
)
