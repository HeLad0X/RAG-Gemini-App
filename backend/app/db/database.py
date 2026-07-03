from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker  
from sqlalchemy.orm import declarative_base 
from sqlalchemy.engine import URL
from decouple import config

DB_URL = URL.create(
    drivername="postgresql+asyncpg", 
    username=config("DB_USER"),
    password=config("DB_PASSWORD"),
    host=config("DB_HOST"),
    port=config("DB_PORT", cast=int),
    database=config("DB_NAME")
)

engine = create_async_engine(DB_URL) 
SessionLocal = async_sessionmaker(autoflush=False, bind=engine, expire_on_commit=False) 

Base = declarative_base()

async def get_db(): 
    async with SessionLocal() as db:
        yield db
