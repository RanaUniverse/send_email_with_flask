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
)


from flask_login import (  # type: ignore
    login_required,  # type: ignore
    login_user,  # type: ignore
    logout_user,
)

# this below is the demo database

from .services import check_authentication

from .forms import LoginForm

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
            return redirect(url_for("auth_bp.login"))

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


@auth_bp.route(rule="/register", methods=["GET", "POST"])
def register():
    """
    this page is for showing registerariotn page
    """
    return render_template(
        template_name_or_list="auth/register.html",
    )
