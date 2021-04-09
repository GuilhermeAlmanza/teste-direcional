from abc import ABC, abstractmethod

from fastapi.routing import APIRouter


class Controller(ABC):
    def __init__(self, router: APIRouter) -> None:
        self.set_router(router)

    def set_router(self, router: APIRouter):
        self.router = router
        self.include_routes()

    @abstractmethod
    def include_routes(self):
        ...
