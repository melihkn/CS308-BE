from fastapi import FastAPI
# Import the cart_router from the controllers.cart_controller module
from controllers.cart_controller import router as cart_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Shopping Cart Service",
    description="A microservice for managing shopping cart operations",
    version="1.0.0"
)

# Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router from the cart controller
app.include_router(cart_router)

# Run the application with Uvicorn on port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)

# to run this: uvicorn main:app --reload --port 8001

# 