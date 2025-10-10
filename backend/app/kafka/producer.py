import asyncio
from aiokafka import AIOKafkaProducer
import json
from app.kafka.config import KAFKA_BOOTSTRAP_SERVERS

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    loop=loop,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

async def start_producer():
    await producer.start()

async def send_event(topic: str, data: dict):
    await producer.send_and_wait(topic, data)

