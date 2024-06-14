from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class RoleEnum(enum.Enum):
    customer = "customer"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum))

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String, index=True)
    price = Column(Float)
    inventory = Column(Integer)

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    quantity = Column(Integer)
    user = relationship("User", back_populates="cart_items")
    book = relationship("Book")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Float)
    user = relationship("User", back_populates="orders")

User.cart_items = relationship("CartItem", back_populates="user")
User.orders = relationship("Order", back_populates="user")
