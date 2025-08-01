# Generated by Django 5.2 on 2025-06-06 19:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openlibrary_id', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('saved', 'Saved'), ('in_progress', 'In Progress'), ('finished', 'Finished')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_statuses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'openlibrary_id')},
            },
        ),
    ]
