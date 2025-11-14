# routes/order_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_conn import get_db
from models import Order, OrderItem
from schemas import OrderCreate, OrderResponse

order = APIRouter(prefix="/orders", tags=["Orders"])

@order.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        # Create the main order record
        new_order = Order(
            order_no=order.OrderId,
            total=order.total
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create related order items
        for item in order.product:
            order_item = OrderItem(
                order_id=new_order.id,
                varid=item.varid,
                product_id=item.product_id,
                image=item.image,
                unit_price=item.price,
                subtotal=(item.quantity)*(item.price),
                quantity=item.quantity
            )
            db.add(order_item)

        db.commit()
        db.refresh(new_order)
        return new_order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating order: {e}")
