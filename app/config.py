from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Environment variables
MONGO_URI = os.getenv("MONGO_URI")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# ✅ Add these lines for Plaid config
# PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
# PLAID_SECRET = os.getenv("PLAID_SECRET")
# PLAID_ENV = os.getenv("PLAID_ENV")  # e.g. "sandbox"
# PLAID_REDIRECT_URI = os.getenv("PLAID_REDIRECT_URI")

SETU_API_KEY = os.getenv("SETU_API_KEY")
SETU_BASE_URL = os.getenv("SETU_BASE_URL", "https://api.setu.co/aa")