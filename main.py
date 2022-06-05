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

models.Base.metadata.create_all(engine)


app = FastAPI()


@app.get("/blogs", tags=["blogs"])
def get_all_blogs(limit=5, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", tags=["blogs"])
def get_blog_by_id(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    return blog


@app.post("/blog/create", tags=["blogs"])
def create_blog(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", tags=["blogs"])
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"Message": "Blog deleted successfully"}


@app.put("/blog/{id}", tags=["blogs"])
def update_blog(id, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no blog found with id: {id}")
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return {"Message": "Blog updated successfully"}


# ///////////////////////////////////////////////


@app.post("/user/create", tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_pass = Hash.bcrypt(request.password)
    new_user = models.User(
        name=request.name, password=hashed_pass, email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", tags=["user"])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error! no user found with id: {id}")
    return user
