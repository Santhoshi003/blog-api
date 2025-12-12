# 📘 Blog API — FastAPI + PostgreSQL + SQLAlchemy

A clean, production-ready RESTful Blog API built using **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, and **Alembic** for database migrations.  
This project demonstrates professional backend architecture, relationship modeling, and optimized CRUD operations.

This README is intentionally improved, polished, and interview-ready — based fully on your reference, but clearer, more structured, and more professional.

---

# 🚀 Features
### ✅ Core Functionalities
- CRUD operations for **Authors** and **Posts**
- Every Author can have **multiple Posts** (1:N relationship)
- **Cascade Delete:** removing an Author automatically deletes their Posts
- SQLAlchemy ORM with Alembic migrations
- Fully modular router-based architecture
- Dockerized PostgreSQL for instant database setup
- Auto-generated API docs using Swagger/OpenAPI

### ⚡ Enhancements Included
- Strong data validation using Pydantic
- Clean project structure for scalability
- Demo author: **Santhoshi**
- Demo email: **santhoshianaparthi@example.com**
- No Postman dependency — fully testable through Swagger UI

---

# 📂 Project Structure
```
blog-api/
├── app/
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── authors.py
│   │   └── posts.py
│   └── __init__.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── docker-compose.yml
├── requirements.txt
├── README.md
```

---

# 🛠️ Setup Instructions
## 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/blog-api.git
cd blog-api
```

## 2️⃣ Start PostgreSQL using Docker
```bash
docker-compose up -d
```
Database credentials:
```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Database: blogdb
```

## 3️⃣ Create & Activate Virtual Environment
```bash
python -m venv .venv
.venv/Scripts/activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

## 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 5️⃣ Apply Alembic Migrations
```bash
alembic upgrade head
```

## 6️⃣ Start FastAPI Server
```bash
uvicorn app.main:app --reload
```

### ✔️ API Documentation
- Swagger UI → http://127.0.0.1:8000/docs  
- ReDoc → http://127.0.0.1:8000/redoc  

---

# 🗄️ Database Schema

## **Authors Table**
| Column      | Type      | Notes                     |
|-------------|-----------|---------------------------|
| id          | Integer PK | Auto-increment            |
| name        | String     | Required                  |
| email       | String     | Unique                    |
| created_at  | DateTime   | Auto timestamp            |

## **Posts Table**
| Column      | Type      | Notes                                  |
|-------------|-----------|----------------------------------------|
| id          | Integer PK | Auto-increment                         |
| title       | String     | Required                               |
| content     | Text       | Required                               |
| author_id   | ForeignKey | References authors.id (ON DELETE CASCADE) |
| created_at  | DateTime   | Auto timestamp                         |

---

# 🔗 ER Diagram (Text-Based)
```
+-----------+        1     N       +-----------+
| Authors   | -------------------> |  Posts    |
+-----------+                      +-----------+
| id (PK)   |                      | id (PK)   |
| name      |                      | title     |
| email     |                      | content   |
| created_at|                      | author_id |
+-----------+                      | created_at|
                                   +-----------+
```

---

# 📚 API Documentation (via Swagger UI)

---

# 👤 AUTHORS ENDPOINTS

### ➤ Create Author  
**POST /authors**
```json
{
  "name": "Santhoshi",
  "email": "santhoshianaparthi@example.com"
}
```

### ➤ Get All Authors  
GET /authors

### ➤ Get Author by ID  
GET /authors/{id}

### ➤ Update Author  
PUT /authors/{id}
```json
{
  "name": "Santhoshi Updated",
  "email": "santhoshianaparthi@example.com"
}
```

### ➤ Delete Author (Cascade)  
DELETE /authors/{id}
```json
{ "message": "Author and all posts deleted successfully" }
```

### ➤ Get All Posts of an Author  
GET /authors/{id}/posts

---

# 📝 POSTS ENDPOINTS

### ➤ Create Post  
POST /posts
```json
{
  "title": "My First Blog",
  "content": "This is my first blog post!",
  "author_id": 1
}
```

### ➤ Get All Posts  
GET /posts  
Filter:  
```
/posts?author_id=1
```

### ➤ Get Post by ID  
GET /posts/{id}
```json
{
  "id": 1,
  "title": "My First Blog",
  "content": "This is my first blog post!",
  "author_id": 1,
  "author": {
    "id": 1,
    "name": "Santhoshi",
    "email": "santhoshianaparthi@example.com"
  }
}
```

### ➤ Update Post  
PUT /posts/{id}

### ➤ Delete Post  
DELETE /posts/{id}
```json
{ "message": "Post deleted successfully" }
```

---

# ⚙️ Alembic Migrations
Generate migration:
```bash
alembic revision --autogenerate -m "initial models"
```
Apply migration:
```bash
alembic upgrade head
```

---

# 🔐 Best Practices Implemented
- Environment variables for database configuration  
- Unique email enforcement  
- Cascade delete ensures data integrity  
- Clean modular routers  
- SQLAlchemy ORM with proper relational mapping  

---

# 🎯 Conclusion
This API provides a clean, scalable, production-ready backend structure built on FastAPI.  
All CRUD features, relationship handling, cascade deletes, validation, and migrations follow strong backend engineering standards.

---

If you want:
✅ A downloadable README.md file  
✅ A GitHub badge section  
✅ A ZIP containing the entire starter project

Just tell me! 🚀
