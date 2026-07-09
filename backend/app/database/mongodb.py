from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = None
db = None

async def connect_database():
    global client
    global db

    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    print("DB connected")

async def close_database():
    client.close()


def get_database():
    return db