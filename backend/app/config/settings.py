from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT:int
    MONGO_URI:str
    DB_NAME:str
    PINECONE_API_KEY: str
    PINECONE_INDEX: str
    GEMINI_API_KEY:str
    class Config:
        env_file=".env"

settings = Settings()