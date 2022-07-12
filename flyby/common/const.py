
from pydantic import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    LOG_LOCATION: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


#: The logging format.
LOGFORMAT = "[%(asctime)s] [PID %(process)d] [%(threadName)s] [%(name)s] [%(levelname)s] %(message)s"
