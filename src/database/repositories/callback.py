from src.database.entities.callback import Callback
from src.database.repositories.base import Repository
from src.dtos import CallbackBodyDTO

class CallbackRepository(Repository):
    def serialize(self, obj):
        pass
    
    def create(self, callback: CallbackBodyDTO):
        callback = Callback(type=callback.type)
        callback.flush()
        return callback.id