from pony import orm
from src.database import db_client
from datetime import datetime


class Callback(db_client.Entity):  # type: ignore
    type = orm.Required(str)
    received_at = orm.Optional(datetime)

    def before_insert(self):
        self.received_at = datetime.now()
