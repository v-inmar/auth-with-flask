from typing import Optional
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from app.forms.auth import SignupForm
from app.extensions import db
from app.utils.result_utils import Result, Ok, Error
from app.utils.string_utils import generate_random_string
from app.models.user_model import UserModel
from app.models.authid_model import AuthidModel
from app.constants import PID_MAX_LENGTH, PID_MIN_LENGTH, AUTHID_MAX_LENGTH, AUTHID_MIN_LENGTH

class UserService:

    # this is a helper function
    # because in the future, you might want to change authid value to perform "logout on all devices"
    # or if user changed password or email and must logout all devices
    def _gen_new_authid(self) -> Result[AuthidModel, Exception]:
        for _ in range(5):
            result: Result[str, Exception] = generate_random_string(AUTHID_MIN_LENGTH, AUTHID_MAX_LENGTH)
            if isinstance(result, Error):
                return Error(result.error)
            
            value = result.data

            model_result: Result[AuthidModel | None, SQLAlchemyError] = AuthidModel.get_by_value(value=value)
            if isinstance(model_result, Error):
                return Error(model_result.error)
            
            if model_result.data is not None:
                continue
            else:
                new_model_result: Result[AuthidModel, SQLAlchemyError] = AuthidModel.new(value=value)
                if isinstance(new_model_result, Error):
                    return Error(new_model_result.error)
                else:
                    return new_model_result
        return Error(ValueError("Try limit was reached."))



    def create_user_service(self, form: SignupForm) -> Result[UserModel, Exception]:
        try:
            # Generate unique authid
            authid_result: Result[AuthidModel, Exception] = self._gen_new_authid()
            if isinstance(authid_result, Error):
                raise ValueError(authid_result.error)
            auth_model: AuthidModel = authid_result.data
            
                
            # create user with generated pid
            for i in range(5):
                result: Result[str, Exception]  = generate_random_string(PID_MIN_LENGTH, PID_MAX_LENGTH)
                if isinstance(result, Error):
                    raise ValueError(result.error)
                pid_value = result.data
                user_pid_result: Result[UserModel | None, SQLAlchemyError] = UserModel.get_by_pid(pid=pid_value)
                if isinstance(user_pid_result, Error):
                    raise ValueError(user_pid_result.error)
                
                if user_pid_result.data != None:
                    continue
                else:
                    hashed_pw: str = bcrypt.hashpw(str(form.password.data).encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
                    user_result: Result[UserModel, SQLAlchemyError]  = UserModel.new(
                        firstname=str(form.firstname.data).strip(),
                        lastname=str(form.lastname.data).strip(),
                        email=str(form.email.data).lower().strip(),
                        hashed_pw=hashed_pw,
                        pid=pid_value,
                        authid_id=auth_model.id
                    )

                    if isinstance(user_result, Error):
                        raise ValueError(user_result.error)
                    
                    db.session.commit()
                    return user_result
            raise TypeError("Unable to create new user")
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return Error(e)
    
    def reactivate_user(self, user_model: UserModel) -> Result[UserModel, Exception]:
        try:
            user_model.datetime_deactivated = None
            db.session.commit()
            return Ok(user_model)
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return Error(e)
                

    
