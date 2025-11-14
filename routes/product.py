from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_conn import get_db
from models import Product, ProductImage, ProductVariation
from schemas import ProductCreate, ProductResponse
from sqlalchemy.orm import joinedload
product = APIRouter(prefix="/products", tags=["Products"])


@product.post("/create", response_model=ProductResponse)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump(exclude={"images", "variations"}))
    db.add(product)
    db.commit()
    db.refresh(product)

    # add images
    if payload.images:
        for img in payload.images:
            product.images.append(ProductImage(**img.model_dump()))

    # add variations
    if payload.variations:
        for var in payload.variations:
            product.variations.append(ProductVariation(**var.model_dump()))

    db.commit()
    db.refresh(product)
    return product


@product.get("/product/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    return product

@product.get("/allproducts",response_model=List[ProductResponse])
def get_product(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products



@product.get("/category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = (
        db.query(Product).filter(Product.category_id == category_id).options(joinedload(Product.images)).all()
    )
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")

    return products