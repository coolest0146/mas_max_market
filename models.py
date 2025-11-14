from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, Integer, BigInteger, DECIMAL, Text, ForeignKey,
    DateTime, Enum, Boolean, CHAR,JSON
)
from sqlalchemy.orm import relationship, DeclarativeBase
from database_conn import Base

class Base(DeclarativeBase):
    pass


# ---------------- USERS -----------------
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("user", "admin", "investor", name="user_roles"), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete")
    investor = relationship("Investor", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(120))
    phone = Column(String(30))
    country = Column(String(60), default="Tanzania")
    city = Column(String(60))
    address_line = Column(String(190))
    avatar_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user = relationship("User", back_populates="profile")


# ---------------- CATEGORIES/changed to service ----------------
class Category(Base):
    __tablename__ = "categories"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    parent_id = Column(BigInteger, ForeignKey("categories.id", onupdate="CASCADE", ondelete="SET NULL"))
    name = Column(String(120), nullable=False)
    slug = Column(String(140), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    parent = relationship("Category", remote_side=[id])
    products = relationship("Product", back_populates="category")


# ---------------- PRODUCTS -----------------
class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category_id = Column(BigInteger, ForeignKey("categories.id", onupdate="CASCADE", ondelete="SET NULL"))
    name = Column(String(160), nullable=False)
    slug = Column(String(180), unique=True, nullable=False)
    sku = Column(String(64), unique=True, nullable=False)
    description = Column(Text)
    price_cents = Column(Integer, nullable=False)                    
    rating_stars = Column(DECIMAL(3, 1), default=0.0, nullable=False) 
    rating_count = Column(Integer, default=0, nullable=False)         
    type = Column(String(60))                                        
    keywords = Column(JSON, default=list)                            
    size_chart_link = Column(String(255))                             
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variations = relationship("ProductVariation", back_populates="product", cascade="all, delete-orphan")
    stock = relationship("InventoryStock", back_populates="product", uselist=False)


# ---------------- PRODUCT IMAGES -----------------
class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    product = relationship("Product", back_populates="images")


# ---------------- PRODUCT VARIATIONS -----------------
class ProductVariation(Base):
    __tablename__ = "product_variations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    variation_uuid = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False, unique=True)
    image_url= Column(String(255), nullable=False)                    # image path
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    product = relationship("Product", back_populates="variations")


# ---------------- ORDERS -----------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    order_no = Column(String(40), unique=True, nullable=False)
    subtotal = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    shipping_fee = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    discount_total = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    total = Column(DECIMAL(12, 2), nullable=False)
    status = Column(Enum("pending", "paid", "shipped", "delivered", "cancelled", "refunded", name="order_status"),default="pending", nullable=False)
    payment_status = Column(Enum("unpaid", "paid", "refunded", "failed", name="payment_status"),default="unpaid", nullable=False)
    notes = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
    payments = relationship("Payment", back_populates="order", cascade="all, delete")
    shipments = relationship("Shipment", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(12, 2), nullable=False)
    subtotal = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    order = relationship("Order", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    provider = Column(String(40), nullable=False)
    provider_ref = Column(String(120))
    amount = Column(DECIMAL(12, 2), nullable=False)
    currency = Column(CHAR(3), default="TZS", nullable=False)
    status = Column(Enum("initiated", "authorized", "captured", "failed", "refunded", name="payment_status_type"),
                    default="initiated", nullable=False)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    order = relationship("Order", back_populates="payments")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    carrier = Column(String(60))
    tracking_no = Column(String(100))
    status = Column(Enum("pending", "in_transit", "delivered", "failed", name="shipment_status"),default="pending", nullable=False)
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    order = relationship("Order", back_populates="shipments")


# ---------------- INVESTORS -----------------
class Investor(Base):
    __tablename__ = "investors"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), unique=True, nullable=False)
    approved_by_admin = Column(Boolean, default=False, nullable=False)
    approved_at = Column(DateTime)
    notes = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user = relationship("User", back_populates="investor")
    fund_movements = relationship("InvestorFundMovement", back_populates="investor")
    balance = relationship("InvestorBalance", back_populates="investor", uselist=False)


class InvestorFundMovement(Base):
    __tablename__ = "investor_fund_movements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    investor_id = Column(BigInteger, ForeignKey("investors.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    movement_type = Column(Enum("invest", "withdraw", "adjust", name="fund_movement_type"), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    reason = Column(String(160))
    created_by = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    investor = relationship("Investor", back_populates="fund_movements")


class InvestorBalance(Base):
    __tablename__ = "investor_balances"

    investor_id = Column(BigInteger, ForeignKey("investors.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    principal = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    last_recalc_at = Column(DateTime, default=datetime.now(), nullable=False)

    investor = relationship("Investor", back_populates="balance")


class MonthlyProfitPool(Base):
    __tablename__ = "monthly_profit_pool"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    month_key = Column(CHAR(7), unique=True, nullable=False)
    total_sales_delivered = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    gross_profit = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    loss_penalty = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    net_distributable = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    profit_margin_pct = Column(DECIMAL(5, 2), default=20.00, nullable=False)
    status = Column(Enum("pending", "finalized", "distributed", name="profit_pool_status"), default="pending", nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


# ---------------- MONTHLY INVESTOR PAYOUTS -----------------
class MonthlyInvestorPayout(Base):
    __tablename__ = "monthly_investor_payouts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    pool_id = Column(BigInteger, ForeignKey("monthly_profit_pool.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    investor_id = Column(BigInteger, ForeignKey("investors.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    investor_weight = Column(DECIMAL(18, 8), default=0, nullable=False)
    payout_amount = Column(DECIMAL(12, 2), default=0.00, nullable=False)
    status = Column(Enum("pending", "approved", "paid", name="payout_status"), default="pending", nullable=False)
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    __table_args__ = (
        # unique constraint on pool + investor
        {"sqlite_autoincrement": True},
    )

    pool = relationship("MonthlyProfitPool")
    investor = relationship("Investor")


# ---------------- AUDIT LOGS -----------------
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_user_id = Column(BigInteger, ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"))
    entity_type = Column(String(40))
    entity_id = Column(BigInteger)
    action = Column(String(40))
    before_json = Column(String(500))  # SQLAlchemy JSON type requires MySQL 5.7+
    after_json = Column(String(500))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)

    actor_user = relationship("User")


    # ---------------- INVENTORY -----------------
class InventoryLocation(Base):
    __tablename__ = "inventory_locations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    code = Column(String(32), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    location_id = Column(BigInteger, ForeignKey("inventory_locations.id", onupdate="CASCADE", ondelete="SET NULL"))
    movement_type = Column(Enum("in", "out", "adjust", name="movement_type"), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String(160))
    ref_type = Column(String(60))
    ref_id = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)


class InventoryStock(Base):
    __tablename__ = "inventory_stock"

    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    qty_on_hand = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    product = relationship("Product", back_populates="stock")


class InventoryMonthlySnapshot(Base):
    __tablename__ = "inventory_monthly_snapshot"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey("products.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    month_key = Column(CHAR(7), nullable=False)
    closing_stock = Column(Integer, nullable=False)
    monthly_units_sold = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
