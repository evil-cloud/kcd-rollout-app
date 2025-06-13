from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitOps API"
    VERSION: str = "1.0.2"
    ROLLOUT_STRATEGY: str = "v1.0.11"
    ROLLOUT_MESSAGE:  str = "¡Hola mundo desde Argo Rollouts, hola KCD buenas tardes!"
    EXTERNAL_API_URL: str = "https://jsonplaceholder.typicode.com/todos/1"

settings = Settings()
