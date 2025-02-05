from sqlalchemy.orm import Session
from models import Todo
from schemas import create, update
from fastapi import HTTPException

def create(db:Session,todo:create,own_id:int):
    try:
        data=Todo(**todo.dict(),own_id=own_id)
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=f"Error while creating: {str(e)}")

def get(db:Session,todo_id:int,own_id:int):
    data=db.query(Todo).filter(Todo.id==todo_id,Todo.own_id==own_id).first()
    if data is None:
        raise HTTPException(status_code=404,detail=f"data with id {todo_id} not found")
    return data

def get_all(db: Session,own_id:int,skip: int = 0, limit: int = 10):
    return db.query(Todo).filter(Todo.own_id==own_id).offset(skip).limit(limit).all()

def update(db:Session,todo_id:int,todo_update:update,own_id:int):
    data=db.query(Todo).filter(Todo.id==todo_id,Todo.own_id==own_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"data not found")
    for key,value in todo_update.dict(exclude_unset=True).items():
        setattr(data,key,value)
    db.commit()
    db.refresh(data)
    return data

def delete(db:Session,todo_id:int,own_id:int):
    data=db.query(Todo).filter(Todo.id==todo_id,Todo.own_id==own_id).first()
    if not data:
        raise HTTPException(status_code=404,detail=f"data not found")
    db.delete(data)
    db.commit()
    return data

