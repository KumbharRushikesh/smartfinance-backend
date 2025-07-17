from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi

from app.routes import auth_routes
# from app.routes import bank__routes
from app.routes import bank_routes


app = FastAPI()

# Include /auth/signup and /auth/login routes
app.include_router(auth_routes.router, prefix="/auth")
# app.include_router(bank__routes.router, prefix="/api")
app.include_router(bank_routes.router, prefix="/setu")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Swagger security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SmartFinance API",
        version="1.0.0",
        description="API for SmartFinance",
        routes=app.routes,
    )
    # 🔥 ADD this: Define security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 🔥 ADD this: Apply security to all paths
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# 🔥 Re-assign
app.openapi = custom_openapi