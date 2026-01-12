from typing import TypeVar, Type
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from app.utils.result_utils import Result, Error, Ok
from app.extensions import db

T = TypeVar("T", bound="BaseModel")

class BaseModel(db.Model):
    """
    Abstract base model providing common fields for all database tables.

    This class defines standard columns that can be inherited by other
    SQLAlchemy models to avoid redundancy and ensure consistency.

    Attributes:
        id (int): The primary key identifier for each record, automatically incremented.
        datetime_created (datetime): The timestamp recording when the record was created,
            automatically set to the current time on insertion.
    """
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    datetime_created = db.Column(db.DateTime, default=func.now())

    @classmethod
    def get_by_id(cls: Type[T], id: int) -> Result[T | None, SQLAlchemyError]:
        try:
            m = cls.query.filter(cls.id == id).first()
            return Ok(m)
        except SQLAlchemyError as e:
            return Error(e)
    


V = TypeVar("V", bound="ValueBaseModel")

class ValueBaseModel(BaseModel):
    __abstract__ = True

    @classmethod
    def get_by_value(cls: Type[V], value: str) -> Result[V | None, SQLAlchemyError]:
        try:
            m = cls.query.filter(cls.value == value).first()
            return Ok(m)
        except SQLAlchemyError as e:
            return Error(e)


