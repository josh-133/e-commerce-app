import asyncio
from aiokafka import AIOKafkaConsumer
import json
from app.kafka.config import KAFKA_BOOTSTRAP_SERVERS, TOPICS

async def start_consumer():
    consumer = AIOKafkaConsumer(
        TOPICS["orders"],
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="analytics-service",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            if msg.topic.startswith("cart"):
                print("Received cart event ({msg.topic}):", msg.value) 
            else:
                print("Received order event:", msg.value)
    finally:
        await consumer.stop()