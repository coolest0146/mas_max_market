from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class MaterialBase(BaseModel):
    name: str
    material_type: str              # pcb | 3d_printing | cnc
    description: Optional[str] = None
    cost_per_unit: Optional[float] = None
    unit: Optional[str] = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    material_type: Optional[str] = None
    description: Optional[str] = None
    cost_per_unit: Optional[float] = None
    unit: Optional[str] = None

class MaterialResponse(MaterialBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
