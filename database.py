from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase

URL = 'sqlite:///database.db'
engine = create_engine(URL)

Session = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, index=True, default=False)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()