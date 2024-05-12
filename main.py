from fastapi import FastAPI
from routers.user import userRouter
from routers.product import productRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow connections from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(userRouter)
app.include_router(productRouter)


app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a PawnAPI!"}
