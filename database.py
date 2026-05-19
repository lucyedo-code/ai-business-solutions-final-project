#This file will handle the connection to the database. In this case, it's a SQLite DB. Nothing crazy.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase

DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL)
DBModelBase.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)