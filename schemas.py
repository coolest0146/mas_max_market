from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

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

class Token(BaseModel):
    access_token:str
    token_type:str

class Update(BaseModel):
    password:Optional[str]=None
    email:Optional[str]=None
    username:Optional[str]=None
    

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class CategoryResponse(CategoryCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class VariationSchema(BaseModel):
    id: str               # variation_uuid
    image: str

    class Config:
        orm_mode = True


class RatingSchema(BaseModel):
    stars: float
    count: int

class ProductImageSchema(BaseModel):
    image: str

    class Config:
        orm_mode = True


class ProductImageSchema(BaseModel):
    image: str

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    slug: str
    sku: str
    description: Optional[str] = None
    price_cents: int
    rating_stars: Optional[float] = 0.0
    rating_count: Optional[int] = 0
    type: Optional[str] = None
    keywords: Optional[List[str]] = []
    size_chart_link: Optional[str] = None
    is_active: bool = True

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    id: int
    name: str
    image: str
    rating: RatingSchema
    variation: List[VariationSchema]
    priceCents: int
    keywords: List[str]

    class Config:
        orm_mode = True



class OrderItemCreate(BaseModel):
    image: str
    name: str
    price: float
    quantity: int
    varid: str
    product_id:int

class OrderCreate(BaseModel):
    Customer: str
    OrderId: str
    PaymentMethod: str
    PaymentNumber: str
    product: List[OrderItemCreate]
    total:str

class OrderResponse(BaseModel):
    order_no:str
    total:float
    user_id:int

    class Config:
        orm_mode = True

# ---------------- MONTHLY INVESTOR PAYOUTS -----------------
class MonthlyInvestorPayoutBase(BaseModel):
    pool_id: int
    investor_id: int
    investor_weight: float
    payout_amount: float
    status: str
    paid_at: Optional[datetime]


class MonthlyInvestorPayoutCreate(BaseModel):
    pool_id: int
    investor_id: int
    investor_weight: Optional[float] = 0
    payout_amount: Optional[float] = 0.00


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



class CNCResponse(BaseModel):
    id: int
    Quantity: int
    Material: str
    Insert: bool
    Threads_and_Tapped_holes: bool
    Tolerance: bool
    PartMarking: str
    PartAssembly: str
    Finished_appearance: str
    Inspection: str
    Technical_drawing_File: str

    class Config:
        orm_mode = True

class CNCcreate(BaseModel):
  Quantity:int
  MachineType:str
  Material:str
  Insert: bool
  Marking: str
  Tolerance:bool
  Threads: bool
  Assembly: str
  Finishing: str
  Inspection: str
  uri:str
  