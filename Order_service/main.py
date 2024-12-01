# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Order_service.controllers.order_controller import router as order_router
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your actual MySQL connection string
DATABASE_URL = "mysql+pymysql://root:MelihKN_53@localhost:3306/Myvet_db"

# Create an engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the app
app = FastAPI()

# Allow CORS (update with the correct origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database (create tables if they don't exist)
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(order_router, prefix="/api/orders", tags=["Orders"])

# Run the application with Uvicorn on port 8004
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)

