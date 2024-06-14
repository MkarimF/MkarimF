from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, crud, auth

router = APIRouter()

@router.get("/inventory", response_model=List[schemas.Book])
def read_inventory(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.get_inventory(db)
