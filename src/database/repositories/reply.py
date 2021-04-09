from pony.orm.core import TransactionIntegrityError, rollback
from database.entities.reply import Reply
from database.repositories.base import Repository
from dtos import ReplyDTO, APIReplyDTO
from core.settings import logger

class ReplyRepository(Repository):
    def serialize(self, obj):
        pass

    def create(self, dto: ReplyDTO, callback_id: int):
        if Reply.exists(message_id=dto.message_id, received=dto.received):
            logger.warning(f"Received duplicate reply: {dto.message_id}")
        else:
            Reply(**dto.dict(), callback_id=callback_id)
    
    def create_many(self, dtos: list[ReplyDTO], callback_id: int):
        for dto in dtos:
            self.create(dto, callback_id)