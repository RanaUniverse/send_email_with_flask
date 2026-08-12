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


from .exceptions import InvalidEmailError
from .forms import LoginForm, RegisterForm, OTPForm
from .services.services import check_authentication
from .dependencies import registration_service_obj
from .presentation import registration_to_flash

from .enums import AfterRegistrationNextStep

# TODO  i will later change this to call the service which will call the otp


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
    rule="/login-with-password",
    methods=["GET", "POST"],
)
def login_with_password():
    """
    This will take the email id and ask for the password to enter

    Currently this is for coming from register

    I will make this workable with login routes goodly and logically
    """

    email = session.get("pending_login_email")

    if email is None:
        flash(
            "Please Enter your email and password to login",
            "warning",
        )
        return redirect(
            url_for(
                "auth_bp.login",
            )
        )

    form = LoginForm()

    if form.validate_on_submit():  # type: ignore
        password = form.password.data or ""
        user_obj = check_authentication(
            email=email,
            password=password,
        )

        if user_obj:
            login_user(user=user_obj)
            session.pop(
                "pending_login_email",
                None,
            )
            flash(
                "Login Successfull",
                "success",
            )

            return redirect(
                url_for(
                    "general_bp.home_page",
                )
            )

        flash(
            "wrong Password",
            "warning",
        )

    return render_template(
        "auth/login_with_password.html",
        form=form,
        email=email,
    )


@auth_bp.route(
    rule="/register",
    methods=["GET", "POST"],
)
def register():
    """
    this page is for showing registerariotn page to user
    and if registion data submitted then this will shows
    the user the way of verify otp like this
    """
    form = RegisterForm()

    if form.validate_on_submit():  # type: ignore

        try:
            register = registration_service_obj.start_registration(
                email=form.email.data or "",
            )

        except InvalidEmailError as e:
            flash(
                message=str(e),
                category="danger",
            )
            return render_template(
                "auth/register.html",
                form=form,
            )

        # TODO later i will add a step if mail server down or somethign so that i can
        # shows to use another way like this based on this

        information = registration_to_flash(
            result=register,
        )

        flash(
            message=information.message,
            category=information.category,
        )

        if register.next_step == AfterRegistrationNextStep.VERIFY_OTP:

            session["pending_email"] = form.email.data

            return redirect(
                url_for(
                    "auth_bp.verify_otp",
                )
            )

        if register.next_step == AfterRegistrationNextStep.ENTER_PASSWORD:
            session["pending_login_email"] = form.email.data
            return redirect(
                url_for(
                    "auth_bp.login_with_password",
                )
            )

        if register.next_step == AfterRegistrationNextStep.SHOW_ERROR:

            return redirect(
                url_for(
                    "auth_bp.register",
                )
            )

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
    form = OTPForm()

    if email is None:
        flash(
            "You Need to register and then come to verify",
            "danger",
        )
        return redirect(
            url_for(
                "auth_bp.register",
            )
        )

    if form.validate_on_submit():  # type: ignore

        otp = form.otp.data or ""

        try:

            # at the time of registration i saved the pending_email in
            # the sesion so i check this value here to get the email and then otp here
            verify = registration_service_obj.verify_registration_otp(
                email=email,
                submitted_otp=otp,
            )

        except InvalidEmailError as e:
            flash(
                message=str(e),
                category="danger",
            )
            return render_template(
                "auth/verify_otp.html",
                form=form,
            )

        if verify.success():

            flash(
                "OTP verified successfully.",
                "success",
            )
            flash(
                "You Are LOG In Successfully",
                "success",
            )

            session.pop("pending_email", None)

            return redirect(
                url_for(
                    "general_bp.home_page",
                )
            )

        flash(
            "Invalid OTP",
            "danger",
        )

    return render_template(
        "auth/verify_otp.html",
        form=form,
        email=email,
    )
