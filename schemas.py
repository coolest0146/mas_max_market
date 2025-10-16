from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    useremail: EmailStr
    password:str
    roles:Optional[str]=None

class UserRead(UserCreate):
    id: int
    roles:str
    class Config:
        orm_mode = True

class UserRoles(BaseModel):
    roles:str

class UserLogin(BaseModel):
    useremail: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
    class Config:
        orm_core = True

class Update_Password(BaseModel):
    password:str

class Update_Password_Message(BaseModel):
    password:str
    message:str
    class Config:
        orm_core=True

class OrderCreate(BaseModel):
    item:str
    price:int
    quantity:int
    Status:Optional[str]="UNCONFIRMED"


class Product(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None

class ProductRead(Product):
    #created_at:str
    class Config:
        orm_core=True


class ProductUpdate(BaseModel):
    name:Optional[str]=None
    price:Optional[float]=None
