from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:TunahanTunahan987.%2C@127.0.0.1:3306/CS308_Project"


# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Base class for models
Base = declarative_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
