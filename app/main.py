from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy.orm import Session

from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
from app.models import Author, Book

app = FastAPI()


@app.post("/authors/", response_model=dict)
def create_author(name: str, db: Session = Depends(get_db)):
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return {"id": author.id, "name": author.name}


@app.get("/authors/")
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()


@app.put("/authors/{author_id}")
def update_author(author_id: int, name: str, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    author.name = name
    db.commit()
    return {"message": "Author updated successfully"}


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}


@app.post("/books/", response_model=dict)
def create_book(title: str, author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = Book(title=title, author_id=author_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"id": book.id, "title": book.title, "author_id": book.author_id}


@app.get("/books/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.put("/books/{book_id}")
def update_book(book_id: int, title: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = title
    db.commit()
    return {"message": "Book updated successfully"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
