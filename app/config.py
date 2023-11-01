from pydantic_settings import BaseSettings

# A list of env variables to be set
# pydantic treats them in a case-insensitive way
# That's an easy way to check whether we set all the env variables
# by not providing default values, we're forcing it to look into env variables
class Settings(BaseSettings):
    pg_username: str
    pg_password: str
    pg_host: str
    pg_port: str
    pg_database: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()