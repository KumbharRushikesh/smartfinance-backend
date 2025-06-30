from fastapi import APIRouter, HTTPException
from app.models.user import UserIn
from app.services.user_service import create_user, authenticate_user

router = APIRouter()

@router.post("/signup")
async def signup(user: UserIn):
    user_id = await create_user(user.email, user.password)
    if not user_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully", "user_id": user_id}

@router.post("/login")
async def login(user: UserIn):
    print("1st")
    token = await authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": token,
        "token_type": "bearer"  # <-- required for Swagger to work
    }
