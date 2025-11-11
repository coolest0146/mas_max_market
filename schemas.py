from datetime import datetime
from pydantic import BaseModel, EmailStr,Decimal
from typing import Optional, List


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileOut(BaseModel):
    user_id: int
    full_name: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address_line: Optional[str]
    avatar_url: Optional[str]

    class Config:
        from_attributes = True


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    is_active: bool
    category_id: Optional[int]

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    order_no: str
    total: float
    status: str
    payment_status: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True



# ---------------- MONTHLY INVESTOR PAYOUTS -----------------
class MonthlyInvestorPayoutBase(BaseModel):
    pool_id: int
    investor_id: int
    investor_weight: Decimal
    payout_amount: Decimal
    status: str
    paid_at: Optional[datetime]


class MonthlyInvestorPayoutCreate(BaseModel):
    pool_id: int
    investor_id: int
    investor_weight: Optional[Decimal] = 0
    payout_amount: Optional[Decimal] = 0.00


class MonthlyInvestorPayoutOut(MonthlyInvestorPayoutBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------- AUDIT LOGS -----------------
class AuditLogBase(BaseModel):
    actor_user_id: Optional[int]
    entity_type: Optional[str]
    entity_id: Optional[int]
    action: Optional[str]
    before_json: Optional[dict]
    after_json: Optional[dict]


class AuditLogCreate(BaseModel):
    entity_type: str
    entity_id: int
    action: str
    before_json: Optional[dict] = None
    after_json: Optional[dict] = None
    actor_user_id: Optional[int] = None


class AuditLogOut(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

