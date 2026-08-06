from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,

    # Check whether a connection is alive before using it
    pool_pre_ping=True,

    # Recycle connections every 5 minutes
    pool_recycle=300,

    # Keep a small connection pool
    pool_size=5,
    max_overflow=10,

    future=True,
)



