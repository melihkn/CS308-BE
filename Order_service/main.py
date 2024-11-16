# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_controller import router as order_router
from database import engine, Base

# Initialize the app
app = FastAPI()

# Allow CORS (update with the correct origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
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
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8004, reload=True)

