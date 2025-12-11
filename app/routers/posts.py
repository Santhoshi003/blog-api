from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models import Post, Author
from app.schemas import PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["posts"])

# POST /posts
@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(payload: PostCreate, db: AsyncSession = Depends(get_db)):
    # ensure author exists
    q = select(Author).where(Author.id == payload.author_id)
    res = await db.execute(q)
    author = res.scalars().first()
    if not author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="author_id does not exist")

    post = Post(title=payload.title, content=payload.content, author_id=payload.author_id)
    db.add(post)
    try:
        await db.commit()
        # reload the post along with its author to avoid lazy-loading during serialization
        q2 = select(Post).where(Post.id == post.id).options(selectinload(Post.author))
        res2 = await db.execute(q2)
        post = res2.scalars().first()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create post")
    return post

# GET /posts (optionally filter by author_id)
@router.get("", response_model=list[PostRead])
async def list_posts(author_id: int | None = None, db: AsyncSession = Depends(get_db)):
    q = select(Post).options(selectinload(Post.author))
    if author_id is not None:
        q = q.where(Post.author_id == author_id)
    res = await db.execute(q)
    posts = res.scalars().all()
    return posts

# GET /posts/{id}
@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    q = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
    res = await db.execute(q)
    post = res.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

# PUT /posts/{id}
@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, payload: PostUpdate, db: AsyncSession = Depends(get_db)):
    q = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
    res = await db.execute(q)
    post = res.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content

    try:
        await db.commit()
        # refresh with author loaded
        q2 = select(Post).where(Post.id == post.id).options(selectinload(Post.author))
        res2 = await db.execute(q2)
        post = res2.scalars().first()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update post")
    return post

# DELETE /posts/{id}
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    q = select(Post).where(Post.id == post_id)
    res = await db.execute(q)
    post = res.scalars().first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return
