from sqlalchemy.orm import Session
from fastapi import status, HTTPException, APIRouter, BackgroundTasks, Depends
from ..models.library import bookCreate, Book, get_db
from app.background_tasks import update_old_register_log, update_new_register_log, create_register_log

router = APIRouter()

@router.post('/')
async def create_book(background_tasks: BackgroundTasks, data: bookCreate, db: Session = Depends(get_db)):
    register = Book(title=data.title, author=data.author)
    db.add(register)
    background_tasks.add_task(create_register_log, b=register)
    db.commit()
    return {"book created": register.title}

@router.get('/')
async def get_books(db: Session = Depends(get_db)):
    results = db.query(Book).all()
    if results:
        return results
    else: 
        return {"No books registered"}

@router.put('/{id}')
def update_book(id: int, data: bookCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    book = db.query(Book).get(id)
    if book:
        background_tasks.add_task(update_old_register_log, old=book)
        if data.title:
            book.title = data.title
        if data.author:
            book.author = data.author
        db.commit()
        db.refresh(book)
        background_tasks.add_task(update_new_register_log, new=book)
        return {"book updated": book}
    return {"error": "Book not found"}

@router.delete("/{id}")
async def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.session.query(Book).get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {"book deleted": book.title}
    return {"error": "Book not found"}
