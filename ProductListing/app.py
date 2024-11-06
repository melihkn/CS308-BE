from fastapi import FastAPI
from controllers.controllers import router as product_router
import uvicorn

app = FastAPI(title="Product Listing Microservice")

# Register the product router
app.include_router(product_router)

# Root route for health check
@app.get("/")
def health_check():
    return {"message": "Product Listing Microservice is running"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8002, reload=True)
