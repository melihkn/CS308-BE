from fastapi import FastAPI
# Import the cart_router from the controllers.cart_controller module
from .controllers.cart_controller import router as cart_router
# Import the product router 
from .controllers.product_controller import router as product_router  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Shopping Cart Service",
    description="A microservice for managing shopping cart operations",
    version="1.0.0"
)

# Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve static files from the "static" directory which are images
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
'''
With this configuration, any file in the static directory can be accessed via a URL like:
    http://127.0.0.1:8001/static/images/Cat-Litter-Pellet-Litter-Angle-5copy_2000x.jpg in the browser of the machine in which server is running.

These image paths will be stored in the database and used in the frontend to display the images. However,
we only store the relative path according to the static directory. For example:
'images/product123.jpg' -> relative path according to the static directory in the backend directory. 
'''

# Include the router from the cart controller
app.include_router(cart_router)
# Include the product router
app.include_router(product_router)  

# Run the application with Uvicorn on port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8001, reload=True)

# to run this: uvicorn main:app --reload --port 8001