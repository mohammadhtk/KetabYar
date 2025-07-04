import requests
from books.models import UserGenrePreference, BookStatus, AIRecommendationChat
from django.conf import settings
import google.generativeai as genai

def fetch_books_by_genre(genre_slug, limit=10):
    url = f"https://openlibrary.org/subjects/{genre_slug}.json?limit={limit}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json().get("works", [])

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": None,
            "cover": f"https://covers.openlibrary.org/b/id/{book.get('cover_id')}-M.jpg" if book.get("cover_id") else None,
            "bookLink": book.get("key"),
            "author": book.get("authors", [{}])[0].get("name"),
        }
        for book in data
    ]

def get_recommendations_by_genre(user, limit_per_genre=3):
    preferences = UserGenrePreference.objects.filter(user=user)
    all_books = []
    for pref in preferences:
        genre_books = fetch_books_by_genre(pref.genre, limit=limit_per_genre)
        all_books.extend(genre_books)
    return all_books

def get_recommendations_by_history(user, limit=5):
    history = BookStatus.objects.filter(user=user).order_by("-updated_at")[:10]
    openlibrary_ids = [b.openlibrary_id for b in history]
    all_books = []
    for openlibrary_id in openlibrary_ids:
        url = f"https://openlibrary.org/works/{openlibrary_id}.json"
        res = requests.get(url)
        if res.status_code != 200:
            continue
        subjects = res.json().get("subjects", [])
        if not subjects:
            continue
        genre = subjects[0].replace(' ', '_').lower()
        all_books.extend(fetch_books_by_genre(genre, limit=1))
    return all_books[:limit]

def ask_gemini_and_store(user, prompt):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Suggest 5 books for this request:{prompt}\nJust list book titles with author names.")
    reply = response.text.strip()
    AIRecommendationChat.objects.create(user=user, prompt=prompt, response=reply)
    return reply

def get_chat_history(user, page=1, page_size=5):
    qs = AIRecommendationChat.objects.filter(user=user).order_by('-created_at')
    start = (page - 1) * page_size
    end = start + page_size
    return qs[start:end], qs.count()

