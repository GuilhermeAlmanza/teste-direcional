from re import T
from pony import orm
from pony.orm.core import composite_key
from src.database import db_client
from datetime import datetime


class APIMessage(db_client.Entity):  # type: ignore
    id = orm.PrimaryKey(str)
    to = orm.Required(str)
    message = orm.Required(str)
    schedule = orm.Required(datetime)
    reference = orm.Optional(str)
    history = orm.Set(lambda: MessageHistory)


class MessageHistory(db_client.Entity): # type: ignore
    received_at = orm.Optional(datetime)
    status = orm.Required(str)
    status_description = orm.Required(str)
    callback_id = orm.Optional(int, nullable=True)
    message = orm.Required(APIMessage)
    latest = orm.Optional(bool)
    orm.PrimaryKey(message, status)

    def before_insert(self):
        self.received_at = datetime.now()
        self.latest = True