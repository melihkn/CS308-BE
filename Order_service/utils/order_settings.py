from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str = "e8e7e4"  # Use a secure key in production
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60  # Token validity duration
    database_url: str = "mysql+pymysql://root:TunahanTunahan987.%2C@127.0.0.1:3306/CS308_Project"

    class Config:
        env_file = ".env"

settings = Settings()