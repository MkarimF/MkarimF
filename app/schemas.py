from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    price: float
    inventory: int

class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    price: float
    inventory: int

    class Config:
        orm_mode = True

class CartItemCreate(BaseModel):
    book_id: int
    quantity: conint(ge=1)

class CartItem(BaseModel):
    id: int
    book: Book
    quantity: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    cart_items: List[CartItemCreate]

class Order(BaseModel):
    id: int
    user_id: int
    total_price: float

    class Config:
        orm_mode = True
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
