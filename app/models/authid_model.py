from __future__ import annotations
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.base_model import ValueBaseModel
from app.utils.result_utils import Result, Ok, Error
from app.constants import AUTHID_MAX_LENGTH


class AuthidModel(ValueBaseModel):
    '''
    This holds the value that get encoded with the session that
    identifies the user.

    This helps to NOT give out user info (email) or db internals (id)
    '''
    __tablename__ = "authid_model"
    value = db.Column(db.String(AUTHID_MAX_LENGTH, collation='utf8mb4_general_ci'), nullable=False, unique=True) # case insensitive ab == AB
    datetime_ttl = db.Column(db.DateTime, nullable=True, default=None) # MySQL will use this to clean up


    def user(self) -> UserModel|None:
        from app.models.user_model import UserModel
        try:
            return UserModel.query.filter(UserModel.authid_id == self.id).first()
        except SQLAlchemyError as e:
            return None
    

    # can also be a static method but it makes more sense to have cls i.e. AuthidModel.new(...)
    @classmethod
    def new(cls, value: str) -> Result[AuthidModel, SQLAlchemyError]:
        try:
            model = AuthidModel(
                value=value
            )
            db.session.add(model)
            db.session.flush() # only flush here, commit happens in the service caller. No rollback (also happens in caller)
            return Ok(model)
        except SQLAlchemyError as e:
            return Error(e)

