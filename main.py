from fastapi import FastAPI,HTTPException,Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud,models,schemas,auth
from database import engine,get_db 
from auth import curr_user

app=FastAPI(debug=True)
models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/todo/")

@app.post("/todo/", response_model=schemas.response)
def create(todo: schemas.create, db: Session = Depends(get_db),user:models.Users=Depends(curr_user)):
    return crud.create(db, todo,own_id=user.id)

@app.get("/todo/", response_model=list[schemas.response])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),user:models.Users=Depends(curr_user)):
    if skip < 0 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid pagination parameters")
    return crud.get_all(db, skip=skip, limit=limit,own_id=user.id)

@app.get("/todo/{todo_id}", response_model=schemas.response)
def read(todo_id: int, db: Session = Depends(get_db),user:models.Users=Depends(curr_user)):
    return crud.get(db, todo_id,own_id=user.id)

@app.put("/todo/{todo_id}", response_model=schemas.response)
def update(todo_id: int, todo_update: schemas.update, db: Session = Depends(get_db),user:models.Users=Depends(curr_user)):
    return crud.update(db, todo_id, todo_update,own_id=user.id)

@app.delete("/todo/{todo_id}", response_model=schemas.response)
def delete(todo_id: int, db: Session = Depends(get_db),user:models.Users=Depends(curr_user)):
    return crud.delete(db, todo_id,own_id=user.id)
