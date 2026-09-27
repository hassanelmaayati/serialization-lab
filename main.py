from fastapi import FastAPI
from database import Base, engine
import models
from routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="1:M Lab")
app.include_router(books.router)

from database import SessionLocal
from schemas import AuthorCreate

@app.post("/authors/", tags=["Authors"])
def create_author(payload: AuthorCreate):
    db = SessionLocal()
    author = models.Author(**payload.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    db.close()
    return {"id": author.id, "name": author.name}

@app.get("/authors/", tags=["Authors"])
def list_authors():
    db = SessionLocal()
    authors = db.query(models.Author).all()
    result = [{"id": a.id, "name": a.name} for a in authors]
    db.close()
    return result