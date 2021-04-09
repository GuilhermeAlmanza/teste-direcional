from fastapi import APIRouter

from controllers.callbacks_controller import CallbacksController

router = APIRouter()

callbacks_controller = CallbacksController(router)