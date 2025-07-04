import requests
from .categories import PREDEFINED_CATEGORIES
from books.models import BookStatus

def fetch_home_books(limit=10):
    res = requests.get(f'https://openlibrary.org/search.json?q=bestseller&limit={limit}')
    data = res.json()

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": book.get("number_of_pages_median"),
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else None,
            "bookLink": book.get("key")
        }
        for book in data.get("docs", [])
    ]



def search_books_service(query):
    res = requests.get(f"https://openlibrary.org/search.json?q={query}")
    data = res.json()

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": book.get("number_of_pages_median"),
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else None,
            "bookLink": book.get("key")
        }
        for book in data.get("docs", [])[:10]
    ]


import requests


def get_book_detail(book_link):
    import requests

    book_link = book_link.strip('/')
    url = f"https://openlibrary.org/{book_link}.json"
    res = requests.get(url)

    if res.status_code != 200:
        return None

    data = res.json()

    # هندل کردن حالت‌های مختلف description
    description = data.get("description")
    if isinstance(description, dict):
        description = description.get("value")
    elif not isinstance(description, str):
        description = None

    return {
        "title": data.get("title"),
        "pages": data.get("number_of_pages"),
        "year": data.get("created", {}).get("value", "")[:4],
        "size": None,
        "lang": None,
        "description": description,
        "cover": f"https://covers.openlibrary.org/b/id/{data.get('covers', [])[0]}-M.jpg"
        if data.get("covers") else None,
        "categories": [
            {"tag": subject, "link": f"/category/{subject.replace(' ', '_')}"}
            for subject in data.get("subjects", [])
        ]
    }


def get_all_categories():
    return PREDEFINED_CATEGORIES


def fetch_books_by_category(category_link):
    url = f"https://openlibrary.org{category_link}.json?limit=10"
    res = requests.get(url)

    if res.status_code != 200:
        return []

    works = res.json().get("works", [])

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": None,
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_id']}-M.jpg" if book.get("cover_id") else None,
            "bookLink": book.get("key"),
            "description": book.get("description") if isinstance(book.get("description"), str) else (
                book.get("description", {}).get("value") if isinstance(book.get("description"), dict) else None
            )
        }
        for book in works
    ]


def fetch_popular_books(limit=10):
    res = requests.get(f'https://openlibrary.org/search.json?q=popular&limit={limit}')
    data = res.json()

    return [
        {
            "title": book.get("title"),
            "year": book.get("first_publish_year"),
            "pages": book.get("number_of_pages_median"),
            "cover": f"https://covers.openlibrary.org/b/id/{book['cover_i']}-M.jpg" if 'cover_i' in book else None,
            "bookLink": book.get("key")
        }
        for book in data.get("docs", [])
    ]

def get_user_book_statuses(user):
    return BookStatus.objects.filter(user=user)

def set_or_update_book_status(user, openlibrary_id, status):
    instance, _ = BookStatus.objects.update_or_create(
        user=user,
        openlibrary_id=openlibrary_id,
        defaults={"status": status}
    )
    return instance

# def fetch_related_books(openlibrary_id):
#     url = f"https://openlibrary.org/works/{openlibrary_id}/similar_books.json"
#     res = requests.get(url)
#     if res.status_code != 200:
#         return []
#     books = res.json().get("works", [])
#     return [
#         {
#             "title": book.get("title"),
#             "year": book.get("first_publish_year"),
#             "pages": None,
#             "cover": f"https://covers.openlibrary.org/b/id/{book.get('cover_id')}-M.jpg"
#             if book.get("cover_id") else None,
#             "bookLink": book.get("key"),
#         }
#         for book in books
#     ]
def get_related_books_by_subject(openlibrary_id: str, limit: int = 5):
    work_url = f"https://openlibrary.org/works/{openlibrary_id}.json"
    work_res = requests.get(work_url)

    if work_res.status_code != 200:
        return []

    work_data = work_res.json()
    subjects = work_data.get("subjects", [])

    if not subjects:
        return []

    first_subject = subjects[0]
    search_url = f"https://openlibrary.org/subjects/{first_subject.lower().replace(' ', '_')}.json?limit={limit}"
    related_res = requests.get(search_url)

    if related_res.status_code != 200:
        return []

    works = related_res.json().get("works", [])

    return [
        {
            "title": book.get("title"),
            "cover": f"https://covers.openlibrary.org/b/id/{book.get('cover_id')}-M.jpg" if book.get("cover_id") else None,
            "bookLink": book.get("key"),
            "author": book.get("authors", [{}])[0].get("name"),
            "year": book.get("first_publish_year"),
        }
        for book in works if book.get("key") != f"/works/{openlibrary_id}"
    ]
