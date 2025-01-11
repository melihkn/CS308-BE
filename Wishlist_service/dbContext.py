from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models.models import Product, Wishlist, WishlistItem, Customer

DATABASE_URL = "mysql+pymysql://root:1212003dogac35@127.0.0.1:3306/myvet_db"

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
