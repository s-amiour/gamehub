import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes import router
from app.database import DATABASE_URL, Base, engine, SessionLocal
from app.schemas import UserCreate
from app.models import User
from app.service import add_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Convert DATABASE_URL to ./users.db
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_needs_seeding = not os.path.exists(db_path)  # Ask OS for CWD => Search for DATABASE_URL
    
    # Bind the schema to engine
    Base.metadata.create_all(bind=engine)
    
    # Seeding only permissible in local development
    if db_needs_seeding and os.getenv("ENV", "local") == "local":
        db = SessionLocal()
        try:
            if db.query(User).first() is None:
                print(f"First run detected: Seeding initial users into {db_path}...")
                
                admin_data = UserCreate(
                    username="admin",
                    email="admin@example.com",
                    password="supersecret"
                )
                client_one = UserCreate(
                    username="philip",
                    email="philip@example.com",
                    password="supersecret"
                )
                
                add_user(db, admin_data)
                add_user(db, client_one)
                
                print(f"{db.query(User).count()} Records successfully seeded.")
        finally:
            db.close()
    
    # When `yield` is hit, API starts accepting requests
    yield 

app = FastAPI(title="user-service", lifespan=lifespan)
app.include_router(router)