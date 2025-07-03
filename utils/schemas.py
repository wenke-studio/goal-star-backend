from typing import Generic, TypeVar

from ninja import Schema

T = TypeVar("T")


class ListSchema(Schema, Generic[T]):
    items: list[T]


class ObjectSchema(Schema, Generic[T]):
    item: T


class DetailSchema(Schema):
    detail: str
