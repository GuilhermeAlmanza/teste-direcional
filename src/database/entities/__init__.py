from importlib import import_module
from src.core.settings import BASE_DIR
from src.database import db_client

for module in [
    module.name
    for module in (BASE_DIR / "database" / "entities").glob("*.py")
    if module.name != "__init__.py"
]:
    import_module(f'src.database.entities.{module.removesuffix(".py")}')

#db_client.generate_mapping(create_tables=True)
