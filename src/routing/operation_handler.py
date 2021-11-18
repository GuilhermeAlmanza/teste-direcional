from fastapi import APIRouter

from src.controllers.operations_controller import OperationsController

router = APIRouter()
controller = OperationsController(router)


