from fastapi import FastAPI
from app.routes import auth_routes

app = FastAPI()

# Include /auth/signup and /auth/login routes
app.include_router(auth_routes.router, prefix="/auth")
