from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    bot_name: str = Field(..., alias="BOT_NAME")
    discord_token: str = Field(..., alias="DISCORD_TOKEN")
    redis_url: str = Field(..., alias="REDIS_URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() # type: ignore