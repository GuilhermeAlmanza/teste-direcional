from pathlib import Path
from fastapi.templating import Jinja2Templates
from logging import Logger

logger: Logger
BASE_DIR: Path
STATIC_DIR: Path
templates: Jinja2Templates