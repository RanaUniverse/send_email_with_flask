"""
app/features/mail/routes.py

Sending email to any other mail id user will fillup this page and
others things will be here in this repo
"""

from flask import (
    Blueprint,
    flash,
    render_template,
    # redirect,
    # url_for,
)


from .forms import OtpEmailForm
from .service import send_otp_to_email

mail_bp = Blueprint(
    name="mail_bp",
    import_name=__name__,
    template_folder="templates",
)


@mail_bp.route(rule="/otp", methods=["GET", "POST"])
@mail_bp.route(rule="/verify_otp", methods=["GET", "POST"])
def otp_send():
    """
    this is for when i will want to get a otp on a email
    i will get this email or verify this page
    """
    form = OtpEmailForm()

    if form.validate_on_submit():  # type: ignore
        to_addr = form.email.data or ""

        send_otp_to_email(
            to_email=to_addr,
        )

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    message=f"{field.upper()}: {error}",
                    category="danger",
                )

    return render_template(
        template_name_or_list="mail/send_otp.html",
        form=form,
    )


# @mail_bp.route(rule="/mail-send", methods=["GET", "POST"])
# def mail_send():
#     form = SendEmailForm()
#     if form.validate_on_submit():
#         to_address = form.email_to.data
#         subject = form.subject.data
#         body = form.body.data

#         # now i get all the email id, subjec and body
#         # now i will call a fun which will send the mail to the address


# @mail_bp.route(rule="/mail-status", methods=["GET", "POST"])
# def mail_status():
#     pass
#     # TODO
