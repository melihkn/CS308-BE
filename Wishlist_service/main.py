from fastapi import FastAPI
from dbContext import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from controllers.wishlist_controller import router as wishlist_router
from controllers.wishlist_item_controller import router as wishlist_item_router
import uvicorn 

# Initialize FastAPI app
app = FastAPI(
    title="Wishlist Service",
    description="API for managing wishlists in an e-commerce application",
    version="1.0.0"
)

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
app.include_router(wishlist_router, prefix="/api/wishlists", tags=["wishlists"])
app.include_router(wishlist_item_router, prefix="/api/wishlist_items", tags=["wishlist_items"])

# Run the application with Uvicorn on port 8005
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)

# to run: uvicorn main:app --reload --port 8005