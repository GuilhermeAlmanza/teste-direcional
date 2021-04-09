from pony import orm
from core.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

db_client = orm.Database()

db_client.bind(provider="mysql", host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
