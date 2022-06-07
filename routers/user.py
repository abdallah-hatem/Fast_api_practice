from fastapi import APIRouter
from urllib import request
import bcrypt
from fastapi import Depends, FastAPI, status, HTTPException
from typing import Optional
from importlib_metadata import Deprecated
from pydantic import BaseModel
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=["user"])


@router.post("/create", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pass = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, password=hashed_pass, email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no user found with id: {id}")
    return user


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Error! no users found")
    return users
