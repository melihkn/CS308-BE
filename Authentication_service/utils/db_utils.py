# Utilization file for database operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = DATABASE_URL = "mysql+pymysql://root:TunahanTunahan987.%2C@127.0.0.1:3306/CS308_Project"


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
