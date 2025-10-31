import os
from fastapi import FastAPI
from app.controllers import auth_controller
from app.controllers import user_controller
from app.controllers import cart_controller
from app.controllers import product_controller
from app.controllers import order_controller
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.kafka.consumer_worker import KafkaConsumerWorker
from app.kafka.producer import create_topics_if_not_exist

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

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
    create_topics_if_not_exist()
    global kafka_worker
    kafka_broker = os.getenv("KAFKA_BROKER", "kafka:9092")
    kafka_worker = KafkaConsumerWorker(
        bootstrap_servers=kafka_broker,
        topics=["cart_item_added", "cart_item_removed"],
    )
    kafka_worker.start()

@app.on_event("shutdown")
def stop_kafka_consumer():
    if kafka_worker:
        kafka_worker.stop()