import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
import logging

logger = logging.getLogger("uvicorn.error")


BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR.parent / "public"
DB_HOST = os.getenv("DB_HOST", "3.237.104.107")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "guilu")
DB_PASSWORD = os.getenv("DB_PASSWORD", "guilu123$")
DB_NAME = os.getenv("DB_NAME", "pontal")

templates = Jinja2Templates(directory=str(STATIC_DIR))