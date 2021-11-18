from pydantic.types import OptionalInt
from src.database.entities.api_message import APIMessage, MessageHistory
from src.database.repositories.base import Repository
from src.dtos import APIMessageDTO
from src.core.settings import logger


class APIMessageRepository(Repository):
    def serialize(self, obj):
        pass

    def create(self, dto: APIMessageDTO, callback_id: OptionalInt = None):
        if self.is_duplicate(dto, callback_id):
            logger.warning(f"Received duplicate api_message: {dto.id}")
        else:
            api_message = self.get_or_create(dto)
            self.register_history(api_message, dto, callback_id)

    def is_duplicate(self, dto: APIMessageDTO, callback_id: OptionalInt = None):
        if api_message := APIMessage.get(id=dto.id):
            return api_message.history.filter(
                lambda h: h.status == dto.status and h.callback_id == callback_id
            ).count() > 0
        else:
            return False

    def get_or_create(self, dto: APIMessageDTO):
        return APIMessage.get(id=dto.id) or APIMessage(
            id=dto.id,
            to=dto.to,
            message=dto.message,
            schedule=dto.schedule,
            reference=dto.reference,
        )

    def register_history(
        self, api_message: APIMessage, dto: APIMessageDTO, callback_id: OptionalInt
    ):
        for item in api_message.history.select():
            item.latest = False
        MessageHistory(
            status=dto.status,
            status_description=dto.status_description,
            callback_id=callback_id,
            message=api_message,
        )
