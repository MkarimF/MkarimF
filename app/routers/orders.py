from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

@router.post("/orders", response_model=schemas.Order)
def create_order(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    return crud.create_order(db, current_user)

@router.get("/orders", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.get_orders(db, current_user)
