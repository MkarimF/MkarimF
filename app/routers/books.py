from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

@router.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.create_book(db, book)

@router.get("/books", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@router.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, book_id, book)
