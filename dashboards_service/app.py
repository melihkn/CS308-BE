from fastapi import FastAPI
from controllers.discountControllers import router as dashboard_router
from controllers.orderControllers import router as order_router

app = FastAPI()

# Register router from controllers
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Sales Manager Dashboard Service"}