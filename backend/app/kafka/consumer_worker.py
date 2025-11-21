import threading
import json
import logging
from fastapi import HTTPException
from confluent_kafka import Consumer, KafkaError
from app.repositories.cart_repository import CartsRepository
from app.repositories.order_repository import OrdersRepository
from app.models.cart import CartItem
from app.database import SessionLocal
from app.models.order import Order


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

            "order.created": self.handle_order_created,
            "order.updated": self.handle_order_updated,
            "order.deleted": self.handle_order_deleted,
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
        except HTTPException as e:
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
    
    def handle_order_created(self, data):
        db = SessionLocal()
        try:
            repo = OrdersRepository(db)
            
            # Build CartItem models from the event
            cart_items_data = data["cart_items"]
            cart_items = [
                CartItem(
                    product_id=item["product_id"],
                    name=item["name"],
                    quantity=item["quantity"],
                    price_at_time=item.get("price_at_time", 0)
                )
                for item in cart_items_data
            ]

            # ✔ calculate total automatically
            total = sum(item.quantity * item.price_at_time for item in cart_items)

            new_order = Order(
                user_id=data["user_id"],
                cart_items=cart_items,
                total_price=total,
            )
            order = repo.create_order(new_order)

            logger.info(
                f"[Order Created] order_id={order.id}, user_id={data['user_id']}, cart_items={len(cart_items)}"
            )
        except Exception as e:
            logger.error(f"Failed to handle order.created: {e}")
        finally:
            db.close()

    def handle_order_updated(self, data):
        db = SessionLocal()
        try:
            repo = OrdersRepository(db)
            order = repo.get_by_id(data["order_id"])

            if not order:
                logger.warning(f"Order not found: {data['order_id']}")
                return

            updated = repo.update_status(order, data["status"])

            logger.info(f"[Order Updated] order_id={order.id}, status={updated.status}")
        except Exception as e:
            logger.error(f"Failed to handle order.updated: {e}")
        finally:
            db.close()
    
    def handle_order_deleted(self, data):
        db = SessionLocal()
        try:
            repo = OrdersRepository(db)
            order = repo.get_by_id(data["order_id"])

            if not order:
                logger.warning(f"Order not found: {data['order_id']}")
                return

            repo.delete_order(order)

            logger.info(f"[Order Deleted] order_id={data['order_id']}")
        except Exception as e:
            logger.error(f"Failed to handle order.deleted: {e}")
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