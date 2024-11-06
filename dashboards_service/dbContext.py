from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual MySQL connection string
PWD='Orkun2003'
USR='root'
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost:3306/myvet_db'.format(USR, PWD)

# Create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
