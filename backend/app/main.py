from fastapi import FastAPI
from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import cart_controller
from app.controllers import product_controller
from app.controllers import order_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(cart_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)

@app.get("/")
def root():
    return {"message": "E-commerce backend is running!"}