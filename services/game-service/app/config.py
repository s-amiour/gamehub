from pydantic_settings import BaseSettings

# The moment a Settings obj is init, Pydantic autom looks at one's system env var's (.env),
# searches for variable (Pydantic is smart enough to match uppercase env var to the lowercase Python attribute).
# If it finds DATABASE_URL, it ignores hardcoded string and uses env value; else, falls back to default: "sqlite:///./games.db".
class Settings(BaseSettings):
    env: str = "local"

    database_url: str = "sqlite:///./games.db"
    redis_url: str = "redis://localhost:6379"

    # Added in Module 6 — must match SECRET_KEY in auth-service
    auth_secret_key: str = "dev-secret-change-in-production"

    model_config = {"env_file": ".env", "extra": "ignore"}  # 'ignore' prevents err when encountering other unrelated env var's

settings = Settings()
