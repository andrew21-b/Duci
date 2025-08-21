from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.context.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
