from fastapi import FastAPI
from .routers import users, Auth

app = FastAPI()

app.include_router(users.router)
app.include_router(Auth.router)


@app.get("/")
async def root():
    return "Welcome"
