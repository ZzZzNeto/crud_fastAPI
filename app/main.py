from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from fastapi_sqlalchemy import DBSessionMiddleware, db

engine = create_engine('sqlite:///banco_de_dados.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class bookCreate(BaseModel):
    title: str
    author: str

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url="sqlite:///banco_de_dados.db")

@app.post('/book')
async def create_book(data: bookCreate):
    register = Book(title=data.title, author=data.author)
    db.session.add(register)
    db.session.commit()
    return {"book created": register.title}

@app.get('/book')
async def get_books():
    results = db.session.query(Book).all()
    if results:
        return results
    else: 
        return {"No books registered"}

@app.put('/book/{id}')
async def update_book(id: int, data: bookCreate):
    book = db.session.query(Book).get(id)
    if book:
        if data.title:
            book.title = data.title
        if data.author:
            book.author = data.author
        db.session.commit()
        db.session.refresh(book)
        return {"book updated": book}
    return {"error": "Book not found"}

@app.delete("/book/{id}")
async def delete_book(id: int):
    book = db.session.query(Book).get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {"book deleted": book.title}
    return {"error": "Book not found"}
