from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_conn import get_db

from materials import (
    create_material,
    get_materials,
    get_material_type,
    update_material,
    delete_material,
)

from Material_schemas import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse
)

materials = APIRouter(prefix="/materials", tags=["Materials"])


@materials.post("/create", response_model=MaterialResponse)
def create(data: MaterialCreate, db: Session = Depends(get_db)):
    return create_material(db, data)


@materials.get("/allmaterials", response_model=list[MaterialResponse])
def list_all(db: Session = Depends(get_db)):
    return get_materials(db)


@materials.get("/{material_type}", response_model=List[MaterialResponse])
def read(material_type: str, db: Session = Depends(get_db)):
    material = get_material_type(db, material_type)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@materials.put("/{material_id}", response_model=MaterialResponse)
def update(material_id: int, data: MaterialUpdate, db: Session = Depends(get_db)):
    updated = update_material(db, material_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated


@materials.delete("/{material_id}")
def delete(material_id: int, db: Session = Depends(get_db)):
    deleted = delete_material(db, material_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"message": "Material deleted successfully"}
