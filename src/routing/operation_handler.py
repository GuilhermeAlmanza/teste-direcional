from fastapi import APIRouter

from controllers.operations_controller import OperationsController

router = APIRouter()
controller = OperationsController(router)


