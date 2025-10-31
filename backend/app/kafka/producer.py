import asyncio
import os
import json
import time
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from app.kafka.config import TOPICS
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

producer_config = {
    'bootstrap.servers': KAFKA_BROKER
}

producer = Producer(producer_config)

loop = asyncio.get_event_loop()

def create_topics_if_not_exist():
    admin_client = AdminClient({"bootstrap.servers": "kafka:9092"})
    
    # Check existing topics
    existing_topics = admin_client.list_topics(timeout=10).topics
    new_topics = []
    for topic in TOPICS:
        if topic not in existing_topics:
            new_topics.append(NewTopic(topic, num_partitions=1, replication_factor=1))
    
    if new_topics:
        admin_client.create_topics(new_topics)
        print(f"Created topics: {[t.topic for t in new_topics]}")
        # Give Kafka some time to propagate the topic creation
        time.sleep(3)
    else:
        print(f"Topics already exist: {TOPICS}")

async def start_producer():
    producer.start()

async def send_event(topic: str, data: dict):
    producer.send_and_wait(topic, data)

def delivery_report(err, msg):
    if (err):
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered {msg.value().decode('utf-8')}")
        print(f"Delivered to {msg.topic()} : partition {msg.partition} : at offset {msg.offset}")