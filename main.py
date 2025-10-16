from fastapi import FastAPI, Depends, HTTPException ,status 
from sqlalchemy.orm import Session
from database_conn import  engine ,get_db
import models ,schemas ,oath2 
from pydantic import BaseModel
from routes import auth ,orders,product
# Create the tables in MySQL if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router=auth.USERS)
app.include_router(router=orders.orders)
app.include_router(router=product.product)

