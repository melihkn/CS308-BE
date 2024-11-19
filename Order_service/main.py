# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.order_controller import router as order_router
from utils.db_utils import engine, Base
import uvicorn

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

