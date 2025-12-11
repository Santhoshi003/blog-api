from typing import Optional
from pydantic import BaseModel, EmailStr

# --- Author schemas ---
class AuthorCreate(BaseModel):
    name: str
    email: EmailStr

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class AuthorRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# --- Post schemas ---
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostAuthor(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    author: PostAuthor

    class Config:
        orm_mode = True
