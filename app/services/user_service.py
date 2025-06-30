from app.db import db
from app.auth.auth_handler import hash_password, verify_password, create_token
from bson import ObjectId

async def create_user(email, password):
    existing = await db.users.find_one({"email": email})
    if existing:
        return None
    hashed_pw = hash_password(password)
    user = {"email": email, "password": hashed_pw}
    result = await db.users.insert_one(user)
    return str(result.inserted_id)

async def authenticate_user(email, password):
    print("2nd")
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None
    return create_token(str(user["_id"]))
