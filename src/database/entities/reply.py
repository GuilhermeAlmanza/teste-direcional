from pony import orm
from database import db_client
from datetime import datetime


class Reply(db_client.Entity):  # type: ignore
    message_id = orm.Required(str)
    mailing_id = orm.Required(str)
    mailing_name = orm.Required(str)
    reference = orm.Optional(str)
    classify = orm.Optional(str)
    value = orm.Required(str)
    message = orm.Required(str)
    received = orm.Required(datetime)
    from_ = orm.Required(str, column="from")
    account_id = orm.Required(str)
    account_name = orm.Required(str)
    vars = orm.Optional(orm.Json)
    callback_id = orm.Required(int, unique=True)
    orm.PrimaryKey(message_id, received)
