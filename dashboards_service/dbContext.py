from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual MySQL connection string
DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3306/Myvet_db"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
