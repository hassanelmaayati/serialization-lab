from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import models, schemas


def create_book(db: Session, book: schemas.BookCreate):
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(400, detail="Author not found")

    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(404, detail="Book not found")
    return book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    data = book.model_dump(exclude_unset=True)

    if "author_id" in data:
        author = db.query(models.Author).filter(models.Author.id == data["author_id"]).first()
        if not author:
            raise HTTPException(400, detail="Author not found")

    for key, value in data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    db.delete(db_book)
    db.commit()
    return {"detail": "Book deleted"}