from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BookStatus(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_statuses')
    openlibrary_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'openlibrary_id')


class UserGenrePreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genre_preferences')
    genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} - {self.genre}"


class AIRecommendationChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_chats")
    prompt = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
