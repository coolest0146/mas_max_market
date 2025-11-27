from sqlalchemy.orm import Session
from models import Material
from Material_schemas  import MaterialCreate, MaterialUpdate

def create_material(db: Session, data: MaterialCreate):
    new_material = Material(**data.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


def get_materials(db: Session):
    return db.query(Material).all()


def get_material_type(db: Session, material_type: str):
    return db.query(Material).filter(Material.material_type== material_type).all()


def update_material(db: Session, material_id: int, data: MaterialUpdate):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(material, key, value)

    db.commit()
    db.refresh(material)
    return material


def delete_material(db: Session, material_id: int):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        return None

    db.delete(material)
    db.commit()
    return True
