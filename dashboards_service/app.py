from fastapi import FastAPI
from controllers.discountControllers import router as dashboard_router
from controllers.orderControllers import router as order_router
from controllers.productControllers import router as product_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Register router from controllers
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(product_router, prefix= "/api/v1")

@app.get("/")
def read_root():
    return {"message": "Sales Manager Dashboard Service"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8003, reload=True)