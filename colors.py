from sqlalchemy.orm import Session
from models import Color
from Material_schemas  import MaterialCreate, MaterialUpdate

def create_material(db: Session, data: MaterialCreate):
    new_material = Color(**data.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material


def get_materials(db: Session):
    return db.query(Color).all()


def get_material_type(db: Session, material_type: str):
    return db.query(Color).filter(Color.material_type== material_type).all()


def update_material(db: Session, material_id: int, data: MaterialUpdate):
    colors = db.query(Color).filter(Color.id == material_id).first()
    if not colors:
        return None

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(colors, key, value)

    db.commit()
    db.refresh(colors)
    return colors


def delete_material(db: Session, material_id: int):
    material = db.query(Color).filter(Color.id == material_id).first()
    if not material:
        return None

    db.delete(material)
    db.commit()
    return True
