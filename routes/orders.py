from fastapi import APIRouter, Depends,status,HTTPException
from database_conn import get_db
import schemas,models,oath2


orders=APIRouter(tags=["ORDERS"])

@orders.post("/orders/createOrder")
def create(order_info:schemas.OrderCreate,db=Depends(get_db),id:int=Depends(oath2.get_current_user)):
    order=models.Order(**order_info.model_dump(),user_id=id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@orders.get("/orders/confirmorder/{order_id}")
def Confirm_Order(order_id:int,db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    
    order=db.query(models.Order).filter(models.Order.id==order_id).first()
    user=db.query(models.User).filter(models.User.id==order.user_id).first()
    if not order:
        return HTTPException(status=status.HTTP_204_NO_CONTENT,detail="No orders")
    order.Status="CONFIRMED"
    db.commit()
    db.refresh(order)
    return {f"Dear {user.username} your order with the id { order_id} has been Confirmed"}
    
@orders.get("/orders")
def Confirm_Order(db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    
    orders=db.query(models.Order).all()
    if not orders:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No orders")
    return orders

@orders.get("/orders/{user_ids}")
def Confirm_Order(user_ids:int,db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    
    orders=db.query(models.Order).filter(models.Order.user_id==user_ids).all()
    user=db.query(models.User).filter(models.User.id==models.Order.user_id).first()
    if not orders:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No orders",headers=False)
    return orders
    