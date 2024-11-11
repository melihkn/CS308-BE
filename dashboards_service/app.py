# app/main.py
from fastapi import FastAPI
import uvicorn
from controllers.productControllers import router as product_manager_controller
from controllers.reviewControllers import router as review_controller
from dbContext import engine, Base
from controllers.categoryControllers import router as category_router
from controllers.discountControllers import router as dashboard_router
from controllers.orderControllers import router as order_router
from controllers.salesManagerProductController import router as product_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="MyVet Online Store - Dashboards Service",
    description="API for Product Manager - Sales Manager Dashboards",
    version="1.0.0"
)

# Register router from controllers
app.include_router(dashboard_router, prefix="/SalesManager")
app.include_router(order_router, prefix="/SalesManager")
app.include_router(product_router, prefix= "/SalesManager")
# Include Routers
app.include_router(product_manager_controller, prefix="/ProductManager")
app.include_router(review_controller, prefix="/ProductManager")
app.include_router(category_router, prefix="/ProductManager")

@app.get("/")
def read_root():
    return {"message": "Dashboard Service"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include other routers as needed

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8003, reload=True)


