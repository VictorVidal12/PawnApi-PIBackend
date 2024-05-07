from fastapi import FastAPI
from routers.client import clientRouter
app = FastAPI()
app.include_router(clientRouter)
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a PawnAPI!"}

