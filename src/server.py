from src.core.api import get_application
from uvicorn import run
from src.routing import router

app = get_application(router.routes)


if __name__ == "__main__":
    run("server:app", host="0.0.0.0", port=5000, reload=True)