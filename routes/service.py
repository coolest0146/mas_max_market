import os
from typing import List
import uuid
from fastapi import APIRouter, FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from supabase import create_client
from database_conn import get_db
from models import CNC, Dprinting, Pcbdesign
from schemas import CNCResponse, CNCcreate

SUPABASE_URL = "https://snhcsqjxriwrztyrkejc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNuaGNzcWp4cml3cnp0eXJrZWpjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDUwMzQ1MSwiZXhwIjoyMDc2MDc5NDUxfQ.7KNqimmEo0Y837bLWskA54SPbkjFRPxBuxqqyjuZXHM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET = "Files_technical"

service = APIRouter(prefix="/service", tags=["Services"])
def str_to_bool(value: str) -> bool:
    """Convert string 'true'/'false' to boolean."""
    return value.lower() == "true"

@service.post("/cnc")
async def create_cnc(
    Quantity: str = Form(...),
    MachineType: str = Form(...),
    Material: str = Form(...),
    Insert: str = Form(...),
    Marking: str = Form(...),
    Tolerance: str = Form(...),
    Threads: str = Form(...),
    Assembly: str = Form(...),
    Finishing: str = Form(...),
    Inspection: str = Form(...),
    file: UploadFile = File(None)
    ,db=Depends(get_db)
    ):
    
    file_bytes = await file.read()
    file_name = f"{uuid.uuid4()}_{file.filename}"

    response = supabase.storage.from_(BUCKET).upload(
        file_name,
        file_bytes
    )

    url = supabase.storage.from_(BUCKET).get_public_url(file_name)
    new_order = CNC(
            Designunit = "mm",
            Quantity =Quantity ,
            Color = "white",
            Material =Material ,
            Surface_Finish =Quantity  ,

            Technical_drawing_File =url  ,

            Threads_and_Tapped_holes =str_to_bool(Threads) ,
            Insert =str_to_bool(Insert) ,
            Tolerance = str_to_bool(Tolerance),

            Surface_Roughness = Quantity ,
            PartMarking = Marking, 

            PartAssembly = Assembly,
            Finished_appearance =Finishing, 
            Inspection =Inspection 
        )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
    

@service.post("/printing")
async def create_cnc(
    Quantity: str = Form(...),
    MachineType: str = Form(...),
    Material: str = Form(...),
    Insert: str = Form(...),
    Marking: str = Form(...),
    Tolerance: str = Form(...),
    Threads: str = Form(...),
    Assembly: str = Form(...),
    Finishing: str = Form(...),
    Inspection: str = Form(...),
    file: UploadFile = File(None)
    ,db=Depends(get_db)
    ):
    
    file_bytes = await file.read()
    file_name = f"{uuid.uuid4()}_{file.filename}"

    response = supabase.storage.from_(BUCKET).upload(
        file_name,
        file_bytes
    )

    url = supabase.storage.from_(BUCKET).get_public_url(file_name)
    new_order = Dprinting(
            Designunit = "mm",
            Quantity =Quantity ,
            Color = "white",
            Material =Material ,
            Surface_Finish =Quantity  ,

            Technical_drawing_File =url  ,

            Threads_and_Tapped_holes =str_to_bool(Threads) ,
            Insert =str_to_bool(Insert) ,
            Tolerance = str_to_bool(Tolerance),

            Surface_Roughness = Quantity ,
            PartMarking = Marking, 

            PartAssembly = Assembly,
            Finished_appearance =Finishing, 
            Inspection =Inspection 
        )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
    

@service.post("/pcb")
async def create_cnc(
    Quantity: str = Form(...),
    MachineType: str = Form(...),
    Material: str = Form(...),
    Insert: str = Form(...),
    Marking: str = Form(...),
    Tolerance: str = Form(...),
    Threads: str = Form(...),
    Assembly: str = Form(...),
    Finishing: str = Form(...),
    Inspection: str = Form(...),
    file: UploadFile = File(None)
    ,db=Depends(get_db)
    ):
    
    file_bytes = await file.read()
    file_name = f"{uuid.uuid4()}_{file.filename}"

    response = supabase.storage.from_(BUCKET).upload(
        file_name,
        file_bytes
    )

    url = supabase.storage.from_(BUCKET).get_public_url(file_name)
    new_order = Pcbdesign(
            Designunit = "mm",
            Quantity =Quantity ,
            Color = "white",
            Material =Material ,
            Surface_Finish =Quantity  ,

            Technical_drawing_File =url  ,

            Threads_and_Tapped_holes =str_to_bool(Threads) ,
            Insert =str_to_bool(Insert) ,
            Tolerance = str_to_bool(Tolerance),

            Surface_Roughness = Quantity ,
            PartMarking = Marking, 

            PartAssembly = Assembly,
            Finished_appearance =Finishing, 
            Inspection =Inspection 
        )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order
    