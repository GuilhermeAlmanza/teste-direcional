from abc import ABCMeta, abstractmethod
import inspect
from types import FunctionType
from typing import Any, Callable, Iterable, Optional, TypeVar, Union
from functools import wraps
from pony import orm
from pony.orm import core
import os
from urllib.parse import urlparse

Callable_T = TypeVar("Callable_T")


def db_session(func: Callable_T) -> Callable_T:

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def inner(*args, **kwargs):
            return await (orm.db_session(func))(*args, **kwargs)

    else:

        @wraps(func)
        def inner(*args, **kwargs):
            return orm.db_session(func)(*args, **kwargs)

    return inner


Entity_T = TypeVar("Entity_T", bound="core.Entity")


class MetaRepoDict(dict):
    OPERATIONS = ["_get_db_obj", "query", "get", "create", "update", "delete"]

    def __setitem__(self, k: str, v: ...) -> None:
        if isinstance(v, FunctionType) and k in self.OPERATIONS:
            return super().__setitem__(k, db_session(v))
        else:
            return super().__setitem__(k, v)


class MetaRepository(ABCMeta):
    def __prepare__(metacls, *args, **kwargs):
        return MetaRepoDict()

    def __new__(cls, name: str, bases: list[type], namespace: MetaRepoDict):
        return super().__new__(cls, name, bases, dict(namespace))


class Repository(object, metaclass=MetaRepository):
    Entity: type[core.Entity]

    class Exceptions:
        class DoesNotExist(Exception):
            def __init__(self, *, message: str = "") -> None:
                super().__init__()
                self.message = message

        class RelatedObjectDoesNotExist(Exception):
            def __init__(self, *, field: str, message: str = "") -> None:
                super().__init__()
                self.message = message
                self.field = field

        class AlreadyExists(Exception):
            def __init__(self, *, message: str = "") -> None:
                super().__init__()
                self.message = message

    def filter_query(self, query: list[Entity_T], filters: Iterable["SpecificFilter"]):
        return [
            self.serialize(item)
            for item in query
            if all(filter_item.is_valid(item) for filter_item in filters)
        ]

    def _serialize(self, item: Entity_T) -> dict[str, Union[str, core.Entity]]:
        return item.to_dict(related_objects=True)

    def dict_serialize(self, obj: Entity_T) -> dict[str, Any]:
        serialized = self._serialize(obj)
        return {
            key: value if not isinstance(value, core.Entity) else self._serialize(value)
            for key, value in serialized.items()
        }

    @abstractmethod
    def serialize(self, obj: Entity_T):
        ...

    def _get_db_obj(self, id: Any):
        try:
            return self.Entity[id]
        except orm.ObjectNotFound:
            raise self.Exceptions.DoesNotExist

    def query(self, **kwargs):
        ...

    def get(self, id: Any):
        ...

    def create(self, dto):
        ...

    def update(self, id, dto):
        ...

    def delete(self, id):
        ...


class SpecificFilter:
    def __init__(
        self,
        field: str,
        value: Any,
        related: Optional[str] = None,
        filter_func: Optional[Callable[[Entity_T], bool]] = None,
    ) -> None:
        self.field = field
        self.value = value
        self.related = related
        self.filter_func = filter_func

    def is_valid(self, obj: Entity_T) -> bool:
        if self.value is None:
            return True
        if self.filter_func:
            return self.filter_func(obj)
        if self.related:
            return self._validate_for_related(obj)
        else:
            return self._validate_for_obj(obj)

    def _validate_for_related(self, obj) -> bool:
        return getattr(getattr(obj, self.related, None), self.field, None) == self.value

    def _validate_for_obj(self, obj) -> bool:
        return getattr(obj, self.field, None) == self.value
