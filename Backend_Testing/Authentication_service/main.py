from fastapi import FastAPI
from controllers.auth_controller import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Authentication Service",
    description="A microservice for managing user authentication",
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

# Serve static files from the "static" directory which are images
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
'''
With this configuration, any file in the static directory can be accessed via a URL like:
    http://127.0.0.1:8000/static/images/Cat-Litter-Pellet-Litter-Angle-5copy_2000x.jpg in the browser of the machine in which server is running.

These image paths will be stored in the database and used in the frontend to display the images. However,
we only store the relative path according to the static directory. For example:
'images/product123.jpg' -> relative path according to the static directory in the backend directory. 
'''


# Register the authentication routes
app.include_router(auth_router)

# Run the application with Uvicorn on port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# to run the app, use the following command: uvicorn main:app --reload --port 8000