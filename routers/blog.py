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

router = APIRouter(prefix="/blog", tags=["blogs"])


@router.get("/")
def get_all_blogs(limit=5, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", response_model=schemas.ShowBlog)
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    return blog


@router.post("/create")
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}")
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Blog deleted successfully"}


@router.put("/{id}")
def update_blog(id, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return {"Message": "Blog updated successfully"}
