from fastapi import FastAPI
from routers.user_router import router as user_router

app = FastAPI()

# Include the user router with a prefix
app.include_router(user_router, prefix="/api")

# Root endpoint


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application tiga!"}
