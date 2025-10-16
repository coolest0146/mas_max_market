# models.py
from sqlalchemy import Column, ForeignKey, Integer, String ,Float
from database_conn import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True,unique=True)
    useremail = Column(String(100), unique=True, index=True)
    password  = Column(String(100) ,unique=True)
    roles=Column(String(20) ,server_default="regural")
    image_url=Column(String(255),nullable=True)
    investment = relationship("Investment", back_populates="owner")
    orders=relationship("Order",back_populates="owner")

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    price=Column(Float)
    image_url=Column(String(255),nullable=False)


class Order(Base):
    __tablename__ = "Orders"
    id=Column(Integer,primary_key=True , index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    item=Column(String(100),nullable=False)
    price=Column(Float)
    quantity=Column(Integer)
    Status=Column(String(20))
    owner = relationship("User", back_populates="orders")

class Investment(Base):
    __tablename__="Investement"
    id=Column(Integer,primary_key=True , index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    amount=Column(Float)
    percentage=Column(Float)
    Return=(Float)

    owner = relationship("User", back_populates="investment")






