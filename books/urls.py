from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.books_home, name='books-home'),
    path('home/popular/', views.PopularBooksView.as_view(), name='popular-books'),
    path('search/', views.search_books, name='search-books'),
    path('detail/<path:book_link>/', views.book_detail, name='book-detail'),
    path('categories/', views.all_categories, name='all-categories'),
    path('fetch-category/', views.fetch_category_books, name='fetch-category-books'),
    path('user-books/statuses/', views.user_book_statuses_api, name='user-book-statuses'),
    path('user-books/set-status/', views.set_book_status_api, name='set-book-status'),
    path('related/<str:openlibrary_id>/', views.get_related_books_view, name='related-books'),

]