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
    path('home/', books_home_schema(views.books_home), name='books-home'),
    path('search/', search_books_schema(views.search_books), name='search-books'),
    path('detail/<str:book_link>/', book_detail_schema(views.book_detail), name='book-detail'),
    path('categories/', all_categories_schema(views.all_categories), name='all-categories'),
    path('fetch-category/', fetch_category_books_schema(views.fetch_category_books), name='fetch-category-books'),

]