from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Author, Post
from app.schemas import AuthorCreate, AuthorRead, AuthorUpdate, PostRead

router = APIRouter(prefix="/authors", tags=["authors"])

# POST /authors
@router.post("", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author(payload: AuthorCreate, db: AsyncSession = Depends(get_db)):
    # check unique email
    q = select(Author).where(Author.email == payload.email)
    res = await db.execute(q)
    existing = res.scalars().first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    author = Author(name=payload.name, email=payload.email)
    db.add(author)
    try:
        await db.commit()
        await db.refresh(author)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create author")
    return author


# GET /authors
@router.get("", response_model=list[AuthorRead])
async def list_authors(db: AsyncSession = Depends(get_db)):
    q = select(Author)
    res = await db.execute(q)
    authors = res.scalars().all()
    return authors


# GET /authors/{id}
@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    q = select(Author).where(Author.id == author_id)
    res = await db.execute(q)
    author = res.scalars().first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


# PUT /authors/{id}
@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(author_id: int, payload: AuthorUpdate, db: AsyncSession = Depends(get_db)):
    q = select(Author).where(Author.id == author_id)
    res = await db.execute(q)
    author = res.scalars().first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    # unique email check
    if payload.email and payload.email != author.email:
        q2 = select(Author).where(Author.email == payload.email)
        res2 = await db.execute(q2)
        if res2.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    if payload.name is not None:
        author.name = payload.name
    if payload.email is not None:
        author.email = payload.email

    try:
        await db.commit()
        await db.refresh(author)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update author")

    return author


# DELETE /authors/{id}
@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    q = select(Author).where(Author.id == author_id)
    res = await db.execute(q)
    author = res.scalars().first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    await db.delete(author)
    await db.commit()
    return


# GET /authors/{id}/posts
@router.get("/{author_id}/posts", response_model=list[PostRead])
async def get_author_posts(author_id: int, db: AsyncSession = Depends(get_db)):
    # check author exists
    q = select(Author).where(Author.id == author_id)
    res = await db.execute(q)
    author = res.scalars().first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")

    # get posts with JOIN to author
    q2 = select(Post).where(Post.author_id == author_id).options(selectinload(Post.author))
    res2 = await db.execute(q2)
    posts = res2.scalars().all()
    return posts
