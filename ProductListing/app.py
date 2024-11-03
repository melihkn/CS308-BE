from fastapi import FastAPI
from controllers.controllers import router as product_router

app = FastAPI(title="Product Listing Microservice")

# Register the product router
app.include_router(product_router)

# Root route for health check
@app.get("/")
def health_check():
    return {"message": "Product Listing Microservice is running"}
