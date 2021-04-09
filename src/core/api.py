from json.decoder import JSONDecodeError
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from services import session_manager
from core.settings import STATIC_DIR, logger



def get_application(routes: APIRouter):
    app = FastAPI()

    app.include_router(routes)

    app.mount("/", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.on_event("startup")
    def startup_event():
        logger.info("Starting Session Manager")
        session_manager.init()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Finishing Session Manager")
        await session_manager.finish()


    return app
