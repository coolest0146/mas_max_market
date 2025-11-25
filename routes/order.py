# routes/order_routes.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_conn import get_db
from models import Order, OrderItem
import oath2
from schemas import OrderCreate, OrderResponse
from sqlalchemy.orm import joinedload

from specialschema import OrderSchema
order = APIRouter(prefix="/orders", tags=["Orders"])

@order.post("/create", response_model=List[OrderResponse])
def create_order(order: OrderCreate, db: Session = Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    try:
        # Create the main order record
        new_order = Order(
            order_no=order.OrderId,
            total=order.total,
            user_id=user_id
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create related order items
        for item in order.product:
            order_item = OrderItem(
                order_id=new_order.id,
                variation_id=item.varid,
                product_id=item.product_id,
                unit_price=item.price,
                subtotal=(item.quantity)*(item.price),
                quantity=item.quantity
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return [new_order]

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order: {e}")

#order for the logged inuser 
@order.get("/orders/user")
def get_product(db: Session = Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    orders = (
        db.query(Order).filter(Order.user_id==user_id).options(joinedload(Order.items)).all()
    )
    return orders
#all orders 
@order.get("/orders")
def get_product(db: Session = Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    orders = (
        db.query(Order).options(joinedload(Order.items)).all()
    )
    return orders

#specific user order
@order.get("/orders/{user_id}")
def get_products_by_category(user_id: int, db: Session = Depends(get_db)):
    Orders = (
        db.query(Order).filter(Order.user_id == user_id).options(joinedload(Order.items)).all()
    )
    if not Orders:
        raise HTTPException(status_code=404, detail="No Orders found for this user")

    return Orders

@order.get("/specificorder/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="No Orders found with such id")

    return order