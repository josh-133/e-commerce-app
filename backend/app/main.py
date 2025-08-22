from fastapi import FastAPI
from app.controllers import auth_controller, product_controller, order_controller

app = FastAPI()

app.include_router(auth_controller.router)
# app.include_router(product_controller.router)
# app.include_router(order_controller.router)

@app.get("/")
def root():
    return {"message": "E-commerce backend is running!"}