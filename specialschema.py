from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class OrderItemSchema(BaseModel):
    id: int
    product_id: int
    variation_id: str
    quantity: int
    unit_price: float
    subtotal: float
    created_at: datetime

    class Config:
        orm_mode = True


class PaymentSchema(BaseModel):
    id: int
    provider: str
    provider_ref: Optional[str]
    amount: float
    currency: str
    status: str
    paid_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


class ShipmentSchema(BaseModel):
    id: int
    carrier: Optional[str]
    tracking_no: Optional[str]
    status: str
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True

class OrderSchema(BaseModel):
    id: int
    user_id: int
    order_no: str
    subtotal: float
    shipping_fee: float
    discount_total: float
    total: float
    status: str
    payment_status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    items: List[OrderItemSchema] = []
    payments: List[PaymentSchema] = []
    shipments: List[ShipmentSchema] = []

    class Config:
        orm_mode = True
