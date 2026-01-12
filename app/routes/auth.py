from flask import render_template, abort, redirect, url_for, flash, current_app, request
from flask_login import login_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from app.utils.decorator_utils import auth_not_required, auth_required
from app.forms.auth import LoginForm, SignupForm
from app.services.user import UserService
from app.models.user_model import UserModel
from app.utils.result_utils import Result, Error
from app.utils.form_utils import add_field_error
from app.models.user_model import UserModel

@auth_not_required
def signup() -> str:
    form: SignupForm = SignupForm()
    if form.validate_on_submit():
        new_user_result: Result[UserModel, Exception] = UserService().create_user_service(form=form)
        if isinstance(new_user_result, Error):
            current_app.logger.error(new_user_result.error)
            abort(500)
        
        user_model: UserModel = new_user_result.data

        # send verification email can happen here

        login_user(user=user_model, remember=True, fresh=True)
        flash(message=f"Welcome {str(form.firstname.data).strip().title()}", category="primary")
        return redirect(url_for("home_bp.home"))
    return render_template("signup.html", form=form)


@auth_not_required
def login() -> str:
    form: LoginForm = LoginForm()
    if form.validate_on_submit():
        email = str(form.email.data).lower().strip()
        password = str(form.password.data)
        if len(email) < 1:
            form.email.errors = add_field_error(field=form.email, msg="Invalid email and/or password.")
            form.password.errors = add_field_error(field=form.password, msg="Invalid email and/or password.")
        else:
            user_model_result: Result[UserModel | None, SQLAlchemyError] = UserModel.get_by_email(email=email)
            if isinstance(user_model_result, Error):
                abort(500)
            
            if user_model_result.data is None:
                form.email.errors = add_field_error(field=form.email, msg="Invalid email and/or password.")
                form.password.errors = add_field_error(field=form.password, msg="Invalid email and/or password.")
            else:
                user_model: UserModel = user_model_result.data
                if not user_model.check_password(password=password):
                    form.email.errors = add_field_error(field=form.email, msg="Invalid email and/or password.")
                    form.password.errors = add_field_error(field=form.password, msg="Invalid email and/or password.")
                else:
                    # check if user has been deleted
                    if user_model.datetime_deleted:
                        form.email.errors = add_field_error(field=form.email, msg="Invalid email and/or password.")
                        form.password.errors = add_field_error(field=form.password, msg="Invalid email and/or password.")
                    else:
                        # creds good when it gets to here

                        # reactivate user if needed
                        msg: str = None
                        if user_model.datetime_deactivated:
                            reactivate_user_result: Result[UserModel, Exception] = UserService().reactivate_user(user_model=user_model)
                            if isinstance(reactivate_user_result, Error):
                                abort(500)
                            msg = f"Welcome back, {str(user_model.firstname).title()}"
                        else:
                            msg = f"{str(user_model.firstname).title()}, you are now logged in"
                        
                        if not login_user(user=user_model, remember=True, fresh=True):
                            abort(500)
                        
                        flash(message=msg, category="primary")
                        next_page = request.args.get("next")
                        if next:
                            return redirect(next_page or url_for('home_bp.home'))
                        return redirect(url_for("home_bp.home"))

    return render_template("login.html", form=form)


@auth_required
def logout() -> str:
    logout_user()
    flash(message="You are now logged out", category="primary")
    return redirect(url_for("auth_bp.login"))