# 📚 Book Recommendation & User Management API

This project is a powerful API for user management and book recommendations.  
Using the OpenLibrary API, it provides features such as searching books, viewing detailed book information, browsing categories, and getting smart recommendations based on genres, user reading history, and custom user queries.  
It also includes a full user registration system, account activation, password reset, password change, and avatar management.

---

## 🔥 Features

- **User Management**
  - Register with email and password
  - Account activation via email verification code
  - Password recovery via email code
  - Password change
  - View and update profile (first name, last name, notification settings)
  - Avatar management (upload, view, delete)

- **Book Recommendation System**
  - Recommend books by user's favorite genres
  - Recommend based on user's reading history
  - AI-powered recommendations via custom prompt (Gemini model)
  - View AI chat history

- **Books and Categories**
  - View bestseller and popular books
  - Search books by query
  - View detailed book info
  - View categories and books by category
  - Get related books for a specific book

- **Rate Limiting (Throttling)**
  - Limit Gemini AI related requests to 20 per user per day

- **API Documentation using drf-spectacular**

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9+
- Django 4.x
- Django REST Framework
- `requests` library
- `Pillow` library (for image processing)
- Google Gemini API client (`google.generativeai`)
- PostgreSQL or compatible database
- SMTP server for sending emails

### Steps

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <project-folder>
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create and fill the `.env` file (see `.env.example` below)

5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

---

## 🚀 API Usage

### User Endpoints

| URL                              | HTTP Method | Description                        |
| -------------------------------- | ----------- | -------------------------------- |
| `/register/`                     | POST        | Register a new user               |
| `/activate/<email>/`             | POST        | Activate account with code       |
| `/resend_activation/`            | POST        | Resend activation code            |
| `/reset-password/`               | POST        | Send reset password code          |
| `/reset-password/code/<email>/` | POST        | Reset password with code          |
| `/users/me/`                    | GET, PUT, PATCH | View and update profile          |
| `/users/me/avatar/`              | POST, GET, DELETE | Manage user avatar (upload/view/delete) |

### Books and Categories

| URL                              | HTTP Method | Description                        |
| -------------------------------- | ----------- | -------------------------------- |
| `/home/`                        | GET         | Get books for home page           |
| `/home/popular/`                | GET         | Get popular books                 |
| `/search/`                     | GET         | Search books                     |
| `/detail/<book_link>/`          | GET         | Get book detail                  |
| `/categories/`                 | GET         | Get all categories               |
| `/fetch-category/`             | POST        | Fetch books by category          |
| `/related/<book_link>/`         | GET         | Get related books                |

### Book Recommendations

| URL                              | HTTP Method | Description                        |
| -------------------------------- | ----------- | -------------------------------- |
| `/recommend/genre/`              | GET         | Recommend books by favorite genres|
| `/recommend/history/`            | GET         | Recommend books by reading history|
| `/recommend/prompt/`             | POST        | AI-powered recommendation prompt  |
| `/recommend/chat/history/`      | GET         | Get AI chat history               |

---

## 📚 Project Structure

- `books/`  
  Models, services, and views related to books and recommendations

- `users/`  
  User management, registration, activation, password reset, avatar, etc.

- `users/utils/`  
  Helper utilities like password validation, avatar validation, email sending, code generation/validation

- `books/utils/`  
  Services for OpenLibrary API and Gemini model interaction

---

## ⚠️ Important Notes

- Email sending requires proper SMTP configuration in `settings.py`.
- Avatar images are limited to 20MB and validated with Pillow.
- Passwords must be at least 8 characters long with uppercase, lowercase letters, and digits.
- Account activation is done by email code after registration.
- Gemini AI requests are rate-limited to 20 per user per day.
- OpenAPI documentation available via drf-spectacular for testing all endpoints.

---

## 📄 .env.example

```env
# General
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key
```
 ✅ Copy this into a file named .env in the project root.

 ⚠️ Never commit your actual .env file to version control!

---

## 🛠 Development & Testing

- The project is modular and written with clean, testable code.
- Unit and integration tests can be added for each module.
- Use tools like Postman or Swagger UI to test the API quickly.

---

## 💬 Contact & Collaboration

Feel free to open issues or contact via email for questions, suggestions, or contributions.

---
## 👨‍💻 Contributors
[Mohammad Hasan Tavakoli](mohammadh.tavakoli81@gmail.com)

[Amir Hosein Pishro](amirhosseinpishroa2001@gmail.com)

---
**Good luck and happy coding!**  
🙏📚✨
