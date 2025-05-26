from django.urls import path
from . import views
from books.utils.swagger_docs import (
    books_home_schema,
    search_books_schema,
    book_detail_schema,
    all_categories_schema,
    fetch_category_books_schema
)


urlpatterns = [
    path('home/', views.books_home, name='books-home'),
    path('search/', views.search_books, name='search-books'),
    path('detail/<path:book_link>/', views.book_detail, name='book-detail'),
    path('categories/', views.all_categories, name='all-categories'),
    path('fetch-category/', views.fetch_category_books, name='fetch-category-books'),

]