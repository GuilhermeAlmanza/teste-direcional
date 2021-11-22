import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
import logging

logger = logging.getLogger("uvicorn.error")


BASE_DIR = Path(__file__).parent.parent
STATIC_DIR = BASE_DIR.parent / "public"
TOKEN = "Key ZGlyZWNpb25hbHByZXdwcHByZDpMUTVUZXNQS1Z5ODVOcWc3djVzNA=="

templates = Jinja2Templates(directory=str(STATIC_DIR))