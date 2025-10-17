import asyncio
from confluent_kafka import Producer

producer_config = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(producer_config)

loop = asyncio.get_event_loop()

async def start_producer():
    await producer.start()

async def send_event(topic: str, data: dict):
    await producer.send_and_wait(topic, data)

def delivery_report(err, msg):
    if (err):
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered {msg.value().decode("utf-8")}")
        print(f"Delivered to {msg.topic()} : partition {msg.partition} : at offset {msg.offset}")