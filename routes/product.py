from typing import List
from fastapi import APIRouter, FastAPI, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from supabase import create_client, Client
from models import Product, ProductImage, ProductVariation  # your SQLAlchemy models
from database_conn import get_db  # your DB session dependency
from datetime import datetime
from schemas import  ProductResponse
from sqlalchemy.orm import joinedload
product = APIRouter(prefix="/products", tags=["Products"])

SUPABASE_URL = "https://snhcsqjxriwrztyrkejc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNuaGNzcWp4cml3cnp0eXJrZWpjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDUwMzQ1MSwiZXhwIjoyMDc2MDc5NDUxfQ.7KNqimmEo0Y837bLWskA54SPbkjFRPxBuxqqyjuZXHM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET = "Files_technical"

@product.post("/create")
async def create_product_endpoint(
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    price_cents: int = Form(...),
    primary_image: UploadFile = File(...),
    variations: list[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    try:
        #Upload primary image to Supabase
        primary_ext = primary_image.filename.split(".")[-1]
        primary_filename = f"products/{uuid4()}.{primary_ext}"
        primary_content = await primary_image.read()
        supabase.storage.from_(BUCKET).upload(primary_filename, primary_content)
        primary_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{primary_filename}"

        #Upload variation images
        variation_urls = []
        for v in variations:
            ext = v.filename.split(".")[-1]
            filename = f"products/{uuid4()}.{ext}"
            content = await v.read()
            supabase.storage.from_(BUCKET).upload(filename, content)
            variation_urls.append(f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{filename}")

        #Create Product in DB
        product = Product(
            name=name,
            slug=slug,
            description=description,
            category_id=category_id,
            price_cents=price_cents,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        #Add primary image
        product_image = ProductImage(
            product_id=product.id,
            image_url=primary_url,
            is_primary=True,
            sort_order=1,
        )
        db.add(product_image)

        #Add variations
        for url in variation_urls:
            product_variation = ProductVariation(
                product_id=product.id,
                image_url=url,
            )
            db.add(product_variation)

        db.commit()
        db.refresh(product)

        return {
            "message": "Product created successfully",
            "product_id": product.id,
            "primary_image": primary_url,
            "variations": variation_urls,
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@product.get("/product/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    return product

@product.get("/allproducts", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    formatted_products = []

    for p in products:
        # primary image
        primary_image = None
        for img in p.images:
            if img.is_primary:
                primary_image = img.image_url
                break

        # if no primary image, use first available
        if not primary_image and p.images:
            primary_image = p.images[0].image_url

        # variations
        variations_list = [
            {
                "id": v.variation_uuid,
                "image": v.image_url
            }
            for v in p.variations
        ]

        # build formatted response
        formatted_products.append({
            "id": p.id,
            "name": p.name,
            "image": primary_image,
            "rating": {
                "stars": float(p.rating_stars),
                "count": p.rating_count
            },
            "variation": variations_list,
            "priceCents": p.price_cents,
            "keywords": p.keywords or []
        })

    return formatted_products



@product.get("/category/{category_id}", response_model=List[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = (
        db.query(Product).filter(Product.category_id == category_id).options(joinedload(Product.images)).all()
    )
    if not products:
        raise HTTPException(status_code=404, detail="No products found for this category")

    return products