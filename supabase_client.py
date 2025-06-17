import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

def get_supabase_client() -> Client:
    """Get Supabase client instance"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Missing Supabase configuration. Check SUPABASE_URL and SUPABASE_ANON_KEY in .env file")
    
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def authenticate_user(email: str, password: str):
    """Authenticate user with email and password"""
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def get_user_profile(user_id: str):
    """Get user profile from profiles table"""
    try:
        supabase = get_supabase_client()
        response = supabase.table('profiles').select('*').eq('id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Profile fetch error: {e}")
        return None

def test_supabase_connection():
    """Test connection to Supabase"""
    try:
        supabase = get_supabase_client()
        # Try to access the profiles table (this will test the connection)
        response = supabase.table('profiles').select('count').execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test connection when run directly
    test_supabase_connection()