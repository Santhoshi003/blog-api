from fastapi import FastAPI
from app.routers.authors import router as authors_router
from app.routers.posts import router as posts_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok"}

# register routers
app.include_router(authors_router)
app.include_router(posts_router)
