
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DATABASE_URL ="mysql+pymysql://root:hachimura89@127.0.0.1:3306/myvet_db"




# Create a new engine instance
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



