import os
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routes import router
from app.config import settings
from app.database import DATABASE_URL, Base, engine, SessionLocal
from app.schemas import GameCreate
from app.models import Game
from app.service import add_game

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    db_needs_seeding = not os.path.exists(db_path)
    
    Base.metadata.create_all(bind=engine)
    
    # Seed
    if db_needs_seeding and settings.env == "local":
        db = SessionLocal()
        try:
            if db.query(Game).first() is None:
                print(f"First run detected: Seeding initial game into {db_path}...")
                
                bb_gold = GameCreate(
                    title="Battle Bears Gold",
                    genre="Multiplayer Shooter",
                    platform="iOS, Android",
                    release_year=2013,
                    cover_url="https://via.placeholder.com/300x400?text=Battle+Bears+Gold"
                )
                
                minecraft = GameCreate(
                    title="Minecraft",
                    genre="Sandbox / Survival",
                    platform="Cross-platform",
                    release_year=2011, # Official full release year
                    cover_url="https://via.placeholder.com/300x400?text=Minecraft"
                )
                
                add_game(db, bb_gold)
                add_game(db, minecraft)
                
                print(f"{db.query(Game).count()} Records successfully seeded.")
        finally:
            db.close()
    
    # When `yield` is hit, API starts accepting requests
    yield 


app = FastAPI(title="game-service", lifespan=lifespan)
# Allows for use of APIRouter to modularize codebase
app.include_router(router)
