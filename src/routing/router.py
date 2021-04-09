from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from core.settings import templates
from routing import callback, operation_handler

routes = APIRouter()


@routes.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "SMS Pontal"}
    )


routes.include_router(operation_handler.router, prefix="/api", tags=["Operations"])
routes.include_router(callback.router, prefix="/api", tags=["Callbacks"])
