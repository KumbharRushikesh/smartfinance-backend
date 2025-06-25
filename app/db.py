from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URI)

# Reference to the database
db = client.smartfinance
