import threading
import json
import time
from confluent_kafka import Consumer, KafkaError

class KafkaConsumerWorker(threading.Thread):
    def __init__(self, bootstrap_servers: str, topics: list, group_id: str = "cart-tracker"):
        threading.Thread.__init__(self) 
        self.daemon = True
        self.bootstrap_servers = bootstrap_servers
        self.topics = topics
        self.group_id = group_id
        self.running = True

        self.consumer = Consumer({
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group_id,
            "auto.offset.reset": 'earliest',
            "enable.auto.commit": True,
        })
        self.consumer.subscribe(self.topics)

    def run(self):
        print(f"Kafka consumer started, subscribed to topics: {self.topics}")
        while self.running:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    continue
            try:
                item = json.loads(msg.value().decode("utf-8"))
                print(f"Received item with id of {item.get('product_id')} and a quantity of {item.get('quantity')} from user with id of {item.get('user_id')}")
            except Exception as e:
                print(f"Failed to parse Kafka message: {e}")

    def stop(self):
        self.running = False
        self.consumer.close()
        print("Kafka consumer stopped")