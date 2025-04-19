import os
import supabase
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def signup_user(email: str, password: str):
    response = supabase.auth.sign_up({"email": email, "password": password})
    return response

def login_user(email: str, password: str):
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return response

def get_current_user():
    session = supabase.auth.get_session()
    return session

def sign_out():
    supabase.auth.sign_out()
