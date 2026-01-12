from __future__ import annotations
import bcrypt
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from flask_login import UserMixin
from flask import current_app
from app.extensions import db
from app.utils.result_utils import Result, Ok, Error
from app.models.base_model import BaseModel
from app.constants import PID_MAX_LENGTH


class UserModel(BaseModel, UserMixin):
    __tablename__ = "user_model"
    firstname = db.Column(db.String(128, collation='utf8mb4_bin'), nullable=False) # case sensitive A != a
    lastname = db.Column(db.String(128, collation='utf8mb4_bin'), nullable=False) # case sensitive A != a
    email = db.Column(db.String(255, collation='utf8mb4_general_ci'), nullable=False, unique=True) # case insenstive a@b.c == A@b.C
    password = db.Column(db.String(255), nullable=False) # hashed value

    pid = db.Column(db.String(PID_MAX_LENGTH, collation='utf8mb4_general_ci'), nullable=False, unique=True) # case insenstive 123 == A123

    datetime_verified = db.Column(db.DateTime, nullable=True)
    datetime_deleted = db.Column(db.DateTime, nullable=True) # soft delete
    datetime_deactivated = db.Column(db.DateTime, nullable=True)

    authid_id = db.Column(db.BigInteger, db.ForeignKey("authid_model.id"), nullable=False, unique=True)

    def authid(self) -> AuthidModel|None:
        from app.models.authid_model import AuthidModel
        try:
            return AuthidModel.query.filter(AuthidModel.id == self.authid_id).first()
        except SQLAlchemyError:
            return None
        

    def get_id(self) -> str|None:
        '''
        Returns string or None.
        This overrides the Flask-Login UserMixin get_id method
        '''
        from app.models.authid_model import AuthidModel
        model: AuthidModel | None = self.authid()
        return str(model.value) if model else None
    
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), str(self.password).encode("utf-8"))
    
    # can also be a static method but it makes more sense to have cls i.e. UserMode.new(...)
    @classmethod
    def new(cls, firstname: str, lastname: str, email: str, hashed_pw: str, pid: str, authid_id: int) -> Result[UserModel, SQLAlchemyError]:
        try:
            model = UserModel(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=hashed_pw,
                pid=pid,
                authid_id=authid_id
            )
            db.session.add(model)
            db.session.flush() # only flush here, commit happens in the service caller. No rollback (also happens in caller)
            return Ok(model)
        except SQLAlchemyError as e:
            return Error(e)
    
    @classmethod
    def get_by_email(cls, email: str) -> Result[Optional[UserModel], SQLAlchemyError]:
        try:
            model = UserModel.query.filter(UserModel.email == email).first()
            return Ok(model)
        except SQLAlchemyError as e:
            return Error(e)
    

    @classmethod
    def get_by_pid(cls, pid: str) -> Result[Optional[UserModel], SQLAlchemyError]:
        try:
            model = UserModel.query.filter(UserModel.pid == pid).first()
            return Ok(model)
        except SQLAlchemyError as e:
            return Error(e)




    