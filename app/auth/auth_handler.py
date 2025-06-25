import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
