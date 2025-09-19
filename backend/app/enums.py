import enum

class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class CartStatus(str, enum.Enum):
    ACTIVE = "active"
    ORDERED = "ordered"
    ABANDONED = "abandoned"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"