from django.urls import path
from . import views
from .recommendation_views import *


urlpatterns = [
    path('home/', views.books_home, name='books-home'),
    path('home/popular/', views.PopularBooksView.as_view(), name='popular-books'),
    path('search/', views.search_books, name='search-books'),
    path('detail/<path:book_link>/', views.book_detail, name='book-detail'),
    path('categories/', views.all_categories, name='all-categories'),
    path('fetch-category/', views.fetch_category_books, name='fetch-category-books'),
    path('user-books/statuses/', views.user_book_statuses_api, name='user-book-statuses'),
    path('user-books/set-status/', views.set_book_status_api, name='set-book-status'),
    path('related/<path:book_link>/', views.get_related_books_view, name='related-books'),
    path('recommend/genre/', recommend_by_genre_view, name='recommend-by-genre'),
    path('recommend/history/', recommend_by_history_view, name='recommend-by-history'),
    path('recommend/prompt/', recommend_by_prompt_view, name='recommend-by-prompt'),
    path('recommend/chat/history/', chat_history_view, name='chatbot-history'),

]