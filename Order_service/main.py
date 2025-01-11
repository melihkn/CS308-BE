# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.order_controller import router as order_router
from controllers.refund_cancel_controller import router as refund_cancel_router
from utils.db_utils import engine, Base
import uvicorn

# Initialize the app
app = FastAPI()

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
app.include_router(order_router, prefix="/api/orders", tags=["Orders"])
app.include_router(refund_cancel_router, tags=["Refund/Cancel"])

# Run the application with Uvicorn on port 8004
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)

# uvicorn main:app --reload --port 8004





"""denemek  için:

{
  "customer_id": "734c8a28-917e-11ef-8816-dd891ae32718",
  "total_price": 30,
  "order_date": "2024-03-01",
  "order_address": "Tuzla Istanbul Turkey",
  "order_address_type": "Home",
  "order_address_name": "Home",
  "payment_status": "pending",
  "invoice_link": null,
  "order_status": 0,
  "items": [
    {
      "product_id": "4d538b34-96a9-11ef-b8ae-7cb7217e15ee",
      "quantity": 2,
      "price_at_purchase": 15
    }
  ]
}

{
  "customer_id": "734c8a28-917e-11ef-8816-dd891ae32718",
  "total_price": 46,
  "order_date": "2024-03-01",
  "order_address": "Sabanci Istanbul Turkey",
  "order_address_type": "Work",
  "order_address_name": "Work",
  "payment_status": "pending",
  "invoice_link": null,
  "order_status": 0,
  "items": [
    {
      "product_id": "4d538b34-96a9-11ef-b8ae-7cb7217e15ee",
      "quantity": 2,
      "price_at_purchase": 15
    },
    {
      "product_id": "57f72870-96a9-11ef-b8ae-7cb7217e15ee",
      "quantity": 1,
      "price_at_purchase": 16
    }
  ]
}

"""
