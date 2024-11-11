from fastapi import FastAPI
from controllers.controllers import router as product_router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Product Listing Microservice")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Use your frontend domain in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Content-Type, Authorization)
)

# Register the product router
app.include_router(product_router)

# Root route for health check
@app.get("/")
def health_check():
    return {"message": "Product Listing Microservice is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
