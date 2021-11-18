import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
import logging

logger = logging.getLogger("uvicorn.error")


BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR.parent / "public"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "pontal")
APP_ID_SMOOCH = "app_617b03f69bbb8400e5ef817b"
SECRET_SMOOCH = "l0DEYtI1hLt1HA8pRViBs2JDKb5o2tEGKjrdu9fbRh-P2ZVvbsXqpYLSaa3DKO8_SKFIDj9rAoPJxaFW9hZy7g"
ID_INTEGRATION_WHATSAPP_SMOOCH = "61795368062f9c00e5f6664f"
ID_SMOOCH = "616f3e2cdd1c7f00e6d01ac1"
TOKEN = "Key ZGlyZWNpb25hbHByZXdwcHByZDpMUTVUZXNQS1Z5ODVOcWc3djVzNA=="

templates = Jinja2Templates(directory=str(STATIC_DIR))