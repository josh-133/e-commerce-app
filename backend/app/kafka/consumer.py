import asyncio
import json
from confluent_kafka import Consumer

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    "group.id": "cart-tracker",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(
    consumer_config
)
consumer.subscribe(["cart_item_added", "cart_item_removed"])
print("Consumer is running and is subscribed to cart_item_added and cart_item_removed topics")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Error: {msg.error()}")
        continue
    
    value = msg.value().decode("utf-8")
    item = json.loads(value)
    print(f"Received item: {item}")