# app/main.py
from fastapi import FastAPI
import uvicorn
from review_controllers.reviewControllers import router as review_controller
from dbContext_Review import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MyVet Online Store - Review Service",
    description="API for Review",
    version="1.0.0"
)
app.include_router(review_controller)

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
    uvicorn.run("app:app", host="localhost", port=8031, reload=True)


