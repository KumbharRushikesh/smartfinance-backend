from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM
from fastapi import Depends, HTTPException, Request
from bson import ObjectId
from fastapi import status
from app.db import db


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id):
    payload = {
        "sub": str(user_id),  # Always convert to string for consistency
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # For PyJWT >= 2.0, `jwt.encode` returns a str; for < 2.0 it returns bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    return token

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # tokenUrl used by Swagger
print(oauth2_scheme)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("Raw token passed:", token)  # Debugging

    if token.startswith("Bearer "):
        token = token[len("Bearer "):] 

    try:
        payload = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user