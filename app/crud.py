from sqlalchemy.orm import Session
from . import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, role=models.RoleEnum.customer)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def create_cart_item(db: Session, cart_item: schemas.CartItemCreate, user: models.User):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.book_id == cart_item.book_id, models.CartItem.user_id == user.id).first()
    if db_cart_item:
        db_cart_item.quantity += cart_item.quantity
    else:
        db_cart_item = models.CartItem(**cart_item.dict(), user_id=user.id)
        db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def get_cart_items(db: Session, user: models.User):
    return db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()

def update_cart_item(db: Session, cart_item_id: int, quantity: int, user: models.User):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id, models.CartItem.user_id == user.id).first()
    if db_cart_item:
        db_cart_item.quantity = quantity
        db.commit()
        db.refresh(db_cart_item)
    return db_cart_item

def delete_cart_item(db: Session, cart_item_id: int, user: models.User):
    db_cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id, models.CartItem.user_id == user.id).first()
    if db_cart_item:
        db.delete(db_cart_item)
        db.commit()
    return db_cart_item

def create_order(db: Session, user: models.User):
    cart_items = get_cart_items(db, user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    db_order = models.Order(user_id=user.id, total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in cart_items:
        book = item.book
        book.inventory -= item.quantity
        db.delete(item)
    db.commit()
    return db_order

def get_inventory(db: Session):
    return db.query(models.Book).all()
