# app/main.py
from fastapi import FastAPI
from controllers.productControllers import router as product_manager_controller
from dbContext import engine, Base

# Create all tables (use Alembic for migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MyVet Online Store - Product Manager Dashboard",
    description="API for Product Manager Dashboard",
    version="1.0.0"
)

# Include Routers
app.include_router(product_manager_controller, prefix="/ProductManager")
# Include other routers as needed
