from sqlalchemy.orm import sessionmaker
from db.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
