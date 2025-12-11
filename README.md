# 📘 Blog API — FastAPI + PostgreSQL + SQLAlchemy

A production-ready RESTful Blog API built using **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, and **Alembic** for migrations.  
This project demonstrates clean API design, proper database modeling, and full CRUD operations for **Authors** and **Posts** with a **one-to-many relationship**.

---

# 🚀 Features
- Fully functional CRUD for **Authors**
- Fully functional CRUD for **Posts**
- One Author → Many Posts (1:N relationship)
- Cascade delete (deleting an author deletes all their posts)
- SQLAlchemy ORM models + Alembic migrations
- Dockerized PostgreSQL for easy setup
- Clean folder structure with routers
- API documented automatically via Swagger/OpenAPI
- Postman collection included (optional)

---

# 📂 Project Structure
blog-api/
│
├── app/
│ ├── db.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── routers/
│ ├── authors.py
│ └── posts.py
│
├── alembic/
│ ├── versions/
│ ├── env.py
│ └── script.py.mako
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── postman_collection.json (optional)


---

# 🛠️ Setup Instructions

## 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/blog-api.git
cd blog-api


---

## 2️⃣ Start PostgreSQL using Docker
The project includes a ready-made **docker-compose.yml**:

docker-compose up -d


PostgreSQL will run at:

host: localhost
port: 5432
user: postgres
password: postgres
database: blogdb

---

## 3️⃣ Create & Activate Virtual Environment
python -m venv .venv
.venv/Scripts/activate

---

## 4️⃣ Install Dependencies
pip install -r requirements.txt

---

## 5️⃣ Apply Database Migrations
Runs Alembic migrations to create tables.

alembic upgrade head

---

## 6️⃣ Start the FastAPI Server
uvicorn app.main:app --reload

### Application Links
- Swagger UI → **http://127.0.0.1:8000/docs**
- ReDoc → **http://127.0.0.1:8000/redoc**
- API Root → **http://127.0.0.1:8000**

---

# 🗄️ Database Schema Explanation

## 🧱 Tables:
### `authors`
| Column    | Type        | Notes |
|-----------|-------------|-------|
| id        | Integer PK  | Auto-increment |
| name      | String      | Required |
| email     | String      | Unique |
| created_at| DateTime    | Auto timestamp |

### `posts`
| Column      | Type        | Notes |
|-------------|-------------|-------|
| id          | Integer PK  | Auto-increment |
| title       | String      | Required |
| content     | Text        | Required |
| author_id   | ForeignKey  | References authors(id), ON DELETE CASCADE |
| created_at  | DateTime    | Auto timestamp |

## 🔗 Relationship
- **One Author → Many Posts**
- Foreign key: `posts.author_id`
- Cascade delete ensures:
  - If an author is deleted → all their posts are automatically deleted.

---

# 🧬 ER Diagram (Text-based)
+-----------+ +-----------+
| Authors | 1 N | Posts |
+-----------+-----------+-----------+
| id (PK) |<--------->| id (PK) |
| name | | title |
| email | | content |
| created_at| | author_id |
+-----------+ | created_at|
+-----------+

---

# 📚 API Documentation

All endpoints are tested and verified.

## AUTHORS

### Create Author  
POST /authors

css
Copy code
Request:
``json
{
  "name": "John Doe",
  "email": "john@example.com"
}

Get All Authors - GET /authors

Get Author by ID - GET /authors/{id}

Update Author - PUT /authors/{id}

Delete Author - DELETE /authors/{id}

POSTS :

Create Post - POST /posts

Request:

{
  "title": "My First Post",
  "content": "Hello World",
  "author_id": 1
}

Get All Posts - GET /posts

Filter by Author - GET /posts?author_id=1

Get Post by ID - GET /posts/{id}

Update Post - PUT /posts/{id}

Delete Post - DELETE /posts/{id}

Get All Posts of an Author- GET /authors/{id}/posts
