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
