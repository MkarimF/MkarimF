from fastapi import FastAPI
from .routers import auth, books, cart, orders, admin


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(cart.router, prefix="/cart", tags=["cart"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.on_event("startup")
def on_startup():
    from .database import Base, engine
    Base.metadata.create_all(bind=engine)

