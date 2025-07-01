from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.api.v1.endpoints import users
app = FastAPI(title="Coffee Shop API")

@app.get("/")
def read_root():
    """
    Root endpoint to chek if the API is running
    """
    return {"message":"Salom Nurullo"}
app.include_router(auth.router,prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")