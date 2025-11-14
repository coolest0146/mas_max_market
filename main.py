from fastapi import FastAPI, Depends, HTTPException ,status 
from sqlalchemy.orm import Session
from database_conn import  engine ,get_db
import models ,schemas ,oath2 
from pydantic import BaseModel
from routes import auth ,product,category
# Create the tables in MySQL if not exists
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def root():
    return {"message": "FastAPI + Supabase app deployed successfully 🚀"}

app.include_router(router=auth.USERS)
app.include_router(router=product.product)
app.include_router(router=category.Categories)

