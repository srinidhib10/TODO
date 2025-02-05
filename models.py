from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Users(Base):
    __tablename__="user"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True)
    hashed_pass=Column(String)
    todos = relationship("Todo", back_populates="own")


class Todo(Base):
    __tablename__="todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    own_id=Column(Integer,ForeignKey('user.id'))
    own=relationship("Users",back_populates="todos")