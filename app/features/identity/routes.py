"""
app/features/identity/routes.py

Here i will keep login related things
"""

from flask import (
    Blueprint,
    flash,
    render_template,
    # request,
    redirect,
    url_for,
    session,
)


from flask_login import (  # type: ignore
    login_required,  # type: ignore
    login_user,  # type: ignore
    logout_user,
)


from .forms import LoginForm, RegisterForm, OTPForm
from .services import check_authentication, start_regisration
from .exceptions import InvalidEmailError

auth_bp = Blueprint(
    name="auth_bp",
    import_name=__name__,
    template_folder="templates",
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    form = LoginForm()

    if form.validate_on_submit():  # type: ignore
        email = form.email.data or ""
        password = form.password.data or ""

        user_obj = check_authentication(
            email=email,
            password=password,
        )

        if user_obj:
            login_user(user=user_obj)
            flash(
                message="Login Successful",
                category="success",
            )
            return redirect(url_for("general_bp.home_page"))
        else:
            flash(
                message="Wrong Credentials",
                category="warning",
            )
            return (
                render_template(
                    template_name_or_list="auth/login.html",
                    form=form,
                ),
                401,
            )

    return render_template(
        template_name_or_list="auth/login.html",
        form=form,
    )


@auth_bp.route(rule="/logout")
@login_required
def logout():
    logout_user()
    flash(
        message="You have been logout goodly",
        category="danger",
    )
    return redirect(location=url_for("general_bp.home_page"))


@auth_bp.route(
    rule="/register",
    methods=["GET", "POST"],
)
def register():
    """
    this page is for showing registerariotn page
    """
    form = RegisterForm()

    if form.validate_on_submit():  # type: ignore

        try:
            start_regisration(email=form.email.data or "")
        except InvalidEmailError as e:
            flash(
                message=str(e),
                category="danger",
            )
            return render_template(
                "auth/register.html",
                form=form,
            )

        session["pending_email"] = "xxx"

        flash(
            message="OTP sent successfully.",
            category="success",
        )

        return redirect(url_for("auth_bp.verify_otp"))

        # i wnat to send otp if the email is right where i shoudl to do i wnat to use ddd and how?

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    message=f"{field.upper()}: {error}",
                    category="danger",
                )

    return render_template(
        template_name_or_list="auth/register.html",
        form=form,
    )


@auth_bp.route(
    "/verify-otp",
    methods=["GET", "POST"],
)
def verify_otp():

    email = session.get("pending_email")

    if email is None:
        return redirect(url_for("auth_bp.register"))

    form = OTPForm()

    if form.validate_on_submit():  # type: ignore

        otp = form.otp.data or ""

        # call your OTPService here

        if otp == "123456":
            flash(
                "OTP verified successfully.",
                "success",
            )

            session.pop("pending_email", None)

            return redirect(url_for("general_bp.home_page"))

        flash(
            "Invalid OTP",
            "danger",
        )

    return render_template(
        "auth/verify_otp.html",
        form=form,
        email=email,
    )
