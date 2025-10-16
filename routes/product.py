from database_conn import get_db
from fastapi import APIRouter ,Depends ,HTTPException,status
import schemas,oath2,models
product=APIRouter(tags=["Products"])


@product.post("/products/create")
def create_product(products:schemas.Product,db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    if user.roles != "admin":
        pass
    product=models.Product(**products.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



@product.post("/products/update/{product_id}",response_model=schemas.ProductRead)
def create_product(product_id:int,product:schemas.ProductUpdate,db=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    if user.roles != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Contact Admin For Access")
    products=db.query(models.Product).filter(models.Product.id == product_id)
    if not products :
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"No such Product with the id {product_id}")
    if product.name is not None:
        products.name=product.name
    if product.price is not None:
        products.price=product.price
    db.commit()
    
    return product



@product.post("/products/delete/{product_id}",response_model=schemas.ProductRead)
def create_product(product_id:int,db=Depends(),user_id:int=Depends(oath2.get_current_user)):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    if user.roles != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Contact Admin For Access")
    products=db.query(models.Product).filter(models.Product.id == product_id)
    if not products :
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"No such Product with the id {product_id}")
    db.delete(products)
    return product



@product.get("/products",response_model=schemas.ProductRead)
def create_product(db=Depends(),user_id:int=Depends(oath2.get_current_user)):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    products=db.query(models.Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="No Products")
    return products


