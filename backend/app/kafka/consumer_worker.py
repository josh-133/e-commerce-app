import threading
import json
import logging
from confluent_kafka import Consumer, KafkaError
from app.repositories.cart_repository import CartsRepository
from app.models.cart import CartItem
from app.database import SessionLocal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cart_consumer")


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

        self.EVENT_HANDLERS = {
            "cart.item_added": self.handle_item_added,
            "cart.item_removed": self.handle_item_removed,
            "cart_item_updated": self.handle_item_updated,
        }

    def handle_item_added(self, data):
        db = SessionLocal()
        try:
            repo = CartsRepository(db)
            cart = repo.get_by_user_id(data['user_id'])
            if not cart:
                cart = repo.create_cart(data['user_id'])
            cart_item_schema = CartItem(**data)
            cart_item = repo.add_item(cart, cart_item_schema)
            logger.info(f"[Added] cart_id={cart.id}, product_id={cart_item.product_id}, qty={cart_item.quantity}, user_id={data['user_id']}")
        except Exception as e:
            logger.error(f"Failed to handle item_added event: {e}")
        finally:
            db.close()

    def handle_item_removed(self, data):
        db = SessionLocal()
        try:
            repo = CartsRepository(db)
            cart = repo.get_by_user_id(data["user_id"])
            if not cart:
                logger.warning(f"Cart not found for user {data['user_id']}")
                return

            cart_item = db.query(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.product_id == data["product_id"]
            ).first()

            if not cart_item:
                logger.warning(f"Cart item not found for cart_id={cart.id}, product_id={data['product_id']}")
                return

            repo.remove_item(cart_item)
            logger.info(f"[Removed] cart_id={cart.id}, product_id={cart_item.product_id}, qty={cart_item.quantity}, user_id={data['user_id']}")
        except Exception as e:
            logger.error(f"Failed to handle cart.item_removed: {e}")
        finally:
            db.close()

    def handle_item_updated(self, data):
        db = SessionLocal()
        try:
            repo = CartsRepository(db)
            cart = repo.get_by_user_id(data["user_id"])
            if not cart:
                logger.warning(f"Cart not found for user {data['user_id']}")
                return

            cart_item = db.query(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.product_id == data["product_id"]
            ).first()

            if not cart_item:
                logger.warning(f"Cart item not found for cart_id={cart.id}, product_id={data['product_id']}")
                return

            updated_item = repo.update_item(cart_item, data["quantity"])
            logger.info(f"[Updated] cart_id={cart.id}, product_id={updated_item.product_id}, qty={updated_item.quantity}, user_id={data['user_id']}")
        except Exception as e:
            logger.error(f"Failed to handle cart.item_updated: {e}")
        finally:
            db.close()

    def run(self):
        print(f"Kafka consumer started, subscribed to topics: {self.topics}")
        while self.running:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.error(f"Kafka error: {msg.error()}")
                continue
            try:
                event = json.loads(msg.value().decode("utf-8"))
                event_type = event.get("event_type")
                data = event.get("data", {})

                handler = self.EVENT_HANDLERS.get(event_type)
                if handler:
                    handler(data)
                else:
                    logger.warning(f"Unknown event_type: {event_type}")
            except Exception as e:
                logger.error(f"Failed to parse Kafka message: {e}")

    def stop(self):
        self.running = False
        self.consumer.close()
        print("Kafka consumer stopped")