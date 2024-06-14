from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

@router.post("/cart", response_model=schemas.CartItem)
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_cart_item(db, cart_item, current_user)

@router.get("/cart", response_model=List[schemas.CartItem])
def read_cart(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.get_cart_items(db, current_user)

@router.put("/cart/{cart_item_id}", response_model=schemas.CartItem)
def update_cart(cart_item_id: int, quantity: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.update_cart_item(db, cart_item_id, quantity, current_user)

@router.delete("/cart/{cart_item_id}", response_model=schemas.CartItem)
def delete_cart(cart_item_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.delete_cart_item(db, cart_item_id, current_user)
