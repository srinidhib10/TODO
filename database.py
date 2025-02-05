from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

db_URL="mysql+pymysql://root:srini123@localhost:3304/TODO"

engine =create_engine(db_URL)
Local=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()
def get_db():
    db=Local()
    try:
        yield db
    finally:
        db.close()




