import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env


def get_env_var(name: str, default: str = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value
