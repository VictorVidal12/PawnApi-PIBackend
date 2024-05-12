from fastapi import FastAPI
from routers.user import userRouter
app = FastAPI()
app.include_router(userRouter)
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a PawnAPI!"}
