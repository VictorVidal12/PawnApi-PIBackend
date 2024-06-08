from fastapi import FastAPI
from routers.user import userRouter
from routers.product import productRouter
from routers.buy import buyRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.offer import offerRouter
from routers.sell import sellRouter
from routers.pawn import pawnRouter
from routers.bill import billRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000","http://127.0.0.1:5173","http://localhost:5173"],  # Allow connections from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(userRouter)
app.include_router(productRouter)
app.include_router(offerRouter)
app.include_router(buyRouter)
app.include_router(sellRouter)
app.include_router(pawnRouter)
app.include_router(billRouter)


app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a PawnAPI!"}
