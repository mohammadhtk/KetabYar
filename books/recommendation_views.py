from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from books.utils.recommendation_services import *
from books.utils.swagger_docs import *
from books.utils.throttling import GeminiUserThrottle

@genre_recommendations_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([GeminiUserThrottle])
def recommend_by_genre_view(request):
    books = get_recommendations_by_genre(request.user, limit_per_genre=3)
    return Response({"ok": True, "data": books})

@history_recommendations_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([GeminiUserThrottle])
def recommend_by_history_view(request):
    books = get_recommendations_by_history(request.user)
    return Response({"ok": True, "data": books})

@prompt_recommendations_schema
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([GeminiUserThrottle])
def recommend_by_prompt_view(request):
    prompt = request.data.get("prompt")
    if not prompt:
        return Response({"ok": False, "message": "Prompt is required"}, status=400)
    reply = ask_gemini_and_store(request.user, prompt)
    return Response({"ok": True, "data": reply})

@chat_history_schema
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history_view(request):
    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 5))
    chats, total = get_chat_history(request.user, page, page_size)
    serialized = [
        {"prompt": c.prompt, "response": c.response, "created_at": c.created_at} for c in chats
    ]
    return Response({"ok": True, "total": total, "page": page, "results": serialized})
