import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declaratice import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
database = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}_{port}/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, binf=engine)

Base = declarative_base()

def get_db():
    print("Obteniendo sesión de base de datos")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("Sesión de base de datos cerrada")