from fastapi import FastAPI
from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import cart_controller
from app.controllers import product_controller
from app.controllers import order_controller
from fastapi.middleware.cors import CORSMiddleware
from app.kafka.consumer_worker import KafkaConsumerWorker

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

@app.on_event("startup")
def start_kafka_consumer():
    global kafka_worker
    kafka_worker = KafkaConsumerWorker(
        bootstrap_servers="localhost:9092",
        topics=["cart_item_added", "cart_item_removed"],
    )
    kafka_worker.start()

@app.on_event("shutdown")
def stop_kafka_consumer():
    if kafka_worker:
        kafka_worker.stop()