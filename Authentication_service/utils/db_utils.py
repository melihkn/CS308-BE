# Utilization file for database operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:1212003dogac35@localhost:3306/my_db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a database session
def get_db():
    """
    Dependency to create a new SQLAlchemy database session.
    Closes the session after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
