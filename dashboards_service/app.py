# app/main.py
from fastapi import FastAPI
import uvicorn
from controllers.productControllers import router as product_manager_controller
from controllers.reviewControllers import router as review_controller
from dbContext import engine, Base
from controllers.categoryControllers import router as category_router


app = FastAPI(
    title="MyVet Online Store - Product Manager Dashboard",
    description="API for Product Manager Dashboard",
    version="1.0.0"
)

@app.get("/")
def main_page():
    return {"message" : "Welcome to the Product Manager Dashboard!"}

# Include Routers
app.include_router(product_manager_controller, prefix="/ProductManager")
app.include_router(review_controller, prefix="/ProductManager")
app.include_router(category_router, prefix="/ProductManager")
# Include other routers as needed

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8003, reload=True)


