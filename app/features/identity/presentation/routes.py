"""
app/features/identity/routes.py

Here i will keep login related things
"""

from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    url_for,
)


from flask_login import (  # type: ignore
    login_required,  # type: ignore
    login_user,  # type: ignore
    logout_user,
)


from ..domain.exceptions import InvalidEmailError
from .forms import LoginForm, RegisterForm, OTPForm
from ..dependencies import RegistrationServiceDep, LoginServiceDep
from .message import registration_to_flash, FlashCategory

from ..domain.enums import AfterRegistrationNextStep
from ..presentation.authentication import FlaskLoginUser

from app.shared.otp.policy import get_otp_policy_obj
from app.shared.otp.enums import OTPPurpose


from app.shared.session.enums import IdentitySessionKey
from app.shared.session.service import (
    set_identity_key as set_identity_key_in_session,
    pop_key as pop_key_from_session,
    get_identity_email as get_identity_email_from_session,
)

# TODO  i will later change this to call the service which will call the otp


auth_bp = Blueprint(
    name="auth_bp",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/identity_static",
)


@auth_bp.route(
    "/login",
    methods=["GET", "POST"],
)
def login(
    login_service: LoginServiceDep,
):

    form = LoginForm()

    if form.validate_on_submit():  # type: ignore
        email = form.email.data or ""
        password = form.password.data or ""

        user_obj = login_service.check_authentication(
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
def login_with_password(
    login_service: LoginServiceDep,
):
    """
    This will take the email id and ask for the password to enter

    Currently this is for coming from register

    I will make this workable with login routes goodly and logically
    """

    email = get_identity_email_from_session(
        IdentitySessionKey.LOGIN_PENDING,
    )

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
        user_obj = login_service.check_authentication(
            email=email,
            password=password,
        )

        if user_obj:
            login_user(
                user=user_obj,
            )
            pop_key_from_session(
                key=IdentitySessionKey.LOGIN_PENDING,
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
def register(
    register_service: RegistrationServiceDep,
):
    """
    this page is for showing registerariotn page to user
    and if registion data submitted then this will shows
    the user the way of verify otp like this
    """
    form = RegisterForm()

    if form.validate_on_submit():  # type: ignore

        try:
            register = register_service.start_registration(
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

            set_identity_key_in_session(
                key=IdentitySessionKey.REGISTER_PENDING,
                email_value=form.email.data or "",
            )

            return redirect(
                url_for(
                    "auth_bp.verify_otp",
                )
            )

        if register.next_step == AfterRegistrationNextStep.ENTER_PASSWORD:
            set_identity_key_in_session(
                key=IdentitySessionKey.LOGIN_PENDING,
            )
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
    # Now here get request is working
    pending_email = get_identity_email_from_session(
        IdentitySessionKey.REGISTER_PENDING,
    )

    if pending_email is not None:
        # later i will add redis checking if possible #TODO
        flash(
            f"📧 Registration pending for {pending_email}. "
            "🔐 Verify the OTP to continue, or 🔄 use a different email.",
            "warning",
        )

        return redirect(url_for("auth_bp.verify_otp"))

    return render_template(
        template_name_or_list="auth/register.html",
        form=form,
    )


@auth_bp.route(
    "/verify-otp",
    methods=["GET", "POST"],
)
def verify_otp(
    register_service: RegistrationServiceDep,
):
    """
    As this function should to run after the registration has done
    so i need to check if user comes externally or not also
    """

    email = get_identity_email_from_session(
        key=IdentitySessionKey.REGISTER_PENDING,
    )

    if email is None:
        flash(
            message="First Register Your Account with Email ID then verify your accoutn",
            category=FlashCategory.WARNING,
        )
        return redirect(
            url_for(
                "auth_bp.register",
            )
        )

    obj = get_otp_policy_obj(
        purpose=OTPPurpose.REGISTER,
    )
    form = OTPForm(
        otp_length=obj.length,
    )

    if form.validate_on_submit():  # type: ignore

        otp = form.otp.data or ""

        try:
            verify = register_service.verify_registration_otp(
                email=email,
                submitted_otp=otp,
            )

        except InvalidEmailError as e:
            flash(
                message=str(e),
                category=FlashCategory.DANGER,
            )

            return render_template(
                "auth/verify_otp.html",
                form=form,
            )

        if verify.success:

            new_user = register_service.add_user_to_db(
                email=email,
            )

            # i need to make sure this is using the flask-login class
            login_user(
                user=FlaskLoginUser(
                    new_user,
                )
            )

            flash(
                "OTP verified successfully.",
                "success",
            )

            flash(
                "You Are LOG In Successfully",
                "success",
            )

            pop_key_from_session(key=IdentitySessionKey.REGISTER_PENDING)

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


@auth_bp.route(
    rule="/change-registration-email",
    methods=[
        "POST",
    ],
)
def change_registration_email():
    """
    When this request will come i need to check if the user
    """
    pop_key_from_session(key=IdentitySessionKey.REGISTER_PENDING)

    flash(
        message="Please enter your new email address and continue the registration.",
        category=FlashCategory.INFO,
    )

    return redirect(url_for("auth_bp.register"))


@auth_bp.route(rule="/resend-registration-otp", methods=["POST"])
def resend_registration_otp(
    register_service: RegistrationServiceDep,
):
    """
    Here i need to decide if the otp sending will done now or not
    then only i will send the otp.
    """
    # TODO: implement OTP resend logic

    flash(
        message="📨 A new OTP will be sent here.",
        category=FlashCategory.INFO,
    )

    return redirect(
        url_for(
            "auth_bp.verify_otp",
        )
    )
