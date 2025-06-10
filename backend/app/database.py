# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# SQLAlchemy Engine
# `connect_args={"check_same_thread": False}` is specific to SQLite,
# not generally needed for PostgreSQL, but included for completeness
# if you were to swap DBs temporarily for development.
# For production PostgreSQL, you'd configure connection pooling more robustly.
engine = create_engine(settings.DATABASE_URL) # , connect_args={"check_same_thread": False})

# SessionLocal class
# Each instance of SessionLocal will be a database session.
# The `autocommit=False` means that the session will not commit
# transactions automatically. You need to call `session.commit()` explicitly.
# `autoflush=False` disables automatic flushing of changes to the database
# before queries, giving you more control.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for declarative models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db # Provide the session to the FastAPI endpoint
    finally:
        db.close() # Ensure the session is closed after the request