# Bookmark Manager API

A secure, RESTful API for managing bookmarks, notes, and code snippets. Built with Flask, MongoDB, and JWT authentication. This project is designed for developers who want to organize their bookmarks, personal notes, and code snippets in a single place, with user authentication and fine-grained access to their data.

---

## Features

- **User Authentication & Registration**  
  - Secure registration and login with hashed passwords (bcrypt).
  - JWT-based authentication for stateless sessions.
  - Token refresh endpoint.

- **Item Management**  
  - CRUD operations for "items" (bookmarks, notes, code snippets).
  - Search, filter, and sort items by type, title, or created date.
  - Tag your items for better organization.

- **Multi-user Isolation**  
  - Each user can view and manage only their own items.
  - Strict access control at the API level.

- **Health Check**  
  - Simple `/api/health/` endpoint to monitor service status.

- **Test Coverage**  
  - Pytest-based test suite for authentication and item APIs.

---

## Tech Stack

- **Backend Framework:** Flask (with Blueprints)
- **Database:** MongoDB (via MongoEngine ODM)
- **Authentication:** Flask-JWT-Extended (JWT access/refresh tokens)
- **Password Hashing:** Flask-Bcrypt
- **CORS:** Flask-CORS
- **Containerization:** Docker, Gunicorn for production serving
- **Testing:** Pytest, pytest fixtures
- **Env Management:** python-dotenv

---

## Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/Pranavchikte/bookmark-manager-api.git
cd bookmark-manager-api
```

### 2. Set up Environment Variables

Create a `.env` file in the root with:

```
MONGO_URI=mongodb://localhost:27017/bookmark_manager
JWT_SECRET_KEY=your_secret_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python run.py
```

### 5. Run with Docker

```bash
docker build -t bookmark-manager-api .
docker run -d -p 5000:5000 --env-file .env bookmark-manager-api
```

---

## API Reference

### Auth

- `POST /api/auth/register`  
  Register a new user.  
  Request: `{ "email": "...", "password": "..." }`
- `POST /api/auth/login`  
  Login and obtain JWT tokens.  
  Request: `{ "email": "...", "password": "..." }`
- `POST /api/auth/refresh`  
  Refresh your JWT access token (requires refresh token).

### Items

- `POST /api/items/`  
  Create a new item.  
  Auth: Bearer token.  
  Request:  
  ```json
  {
    "title": "My Bookmark",
    "item_type": "bookmark|snippet|note",
    "content": "https://example.com",
    "tags": ["personal", "reference"]
  }
  ```
- `GET /api/items/`  
  List your items.  
  Query params: `search`, `type` (`bookmark|snippet|note|all`), `sort` (`title_asc|title_desc|date_asc|date_desc`).  
  Auth: Bearer token.
- `PUT /api/items/<item_id>`  
  Update an item. Auth: Bearer token.
- `DELETE /api/items/<item_id>`  
  Delete an item. Auth: Bearer token.

### Health

- `GET /api/health/`  
  Returns `{ "status": "ok" }` if the service is running.

---

## Data Models

### User

- `email` (string, unique)
- `password` (string, hashed)
- `created_at` (datetime)

### Item

- `owner` (User reference)
- `title` (string)
- `item_type` (string: `bookmark|snippet|note`)
- `content` (string: URL, note, or code)
- `tags` (list of strings)
- `created_at` (datetime)

---

## Testing

- All core endpoints are covered with pytest.
- To run tests:
  ```bash
  pytest
  ```

---

## Deployment

- Use the provided `Dockerfile` for production builds.
- Runs with Gunicorn on port 5000 by default.

---

**Pranav Chikte**

---
