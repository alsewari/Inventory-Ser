import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL not found.")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME not found.")

if not COLLECTION_NAME:
    raise ValueError("COLLECTION_NAME not found.")

client = AsyncIOMotorClient(MONGODB_URL)

database = client[DATABASE_NAME]

inventory_collection = database[COLLECTION_NAME]


async def test_connection():
    await client.admin.command("ping")
    print("MongoDB connection successful")