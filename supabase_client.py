import os 
from supabase import create_client ,Client 
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL=os.getenv("supabase_url")
SUPABASE_SERVICE_ROLE_KEY=os.getenv("secret_key")

supabase:Client=create_client(SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY)