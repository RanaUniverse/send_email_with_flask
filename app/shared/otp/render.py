"""
app/shared/otp/render.py

This is responsible to generate the structer of how the mail
data or message will shows to the user.
"""

from flask import render_template

from .enums import OTPPurpose


from .models import OTPEmailPresentation, RenderedOTPEmail

OTP_EMAIL_PRESENTATION_DICT: dict[OTPPurpose, OTPEmailPresentation] = {
    OTPPurpose.REGISTER: OTPEmailPresentation(
        subject_template="Verify Your email address",
        text_template="emails/otp/register.txt",
        html_template="emails/otp/register.html",
    ),
    OTPPurpose.LOGIN: OTPEmailPresentation(
        subject_template="Your Login verification code",
        text_template="emails/otp/login.txt",
        html_template="emails/otp/login.html",
    ),
    OTPPurpose.FORGET_PASSWORD: OTPEmailPresentation(
        subject_template="Password reset verification code",
        text_template="emails/otp/forget_password.txt",
        html_template="emails/otp/forget_password.html",
    ),
}


def render_otp_email(
    *,
    otp: str,
    valid_seconds: int,
    purpose: OTPPurpose,
) -> RenderedOTPEmail:
    """
    Render the text and HTML Version of the otp mail

    purpose -> This value defines which templates are used

    Raise:
        KeyError when the email template not found
    """

    try:
        presentation = OTP_EMAIL_PRESENTATION_DICT[purpose]
    except KeyError as exc:
        raise ValueError(
            f"No OTP email presentation configured for: {purpose}"
        ) from exc

    body_text = render_template(
        template_name_or_list=presentation.text_template,
        otp=otp,
        valid_seconds=valid_seconds,
    )

    body_html = render_template(
        template_name_or_list=presentation.html_template,
        otp=otp,
        valid_seconds=valid_seconds,
    )

    return RenderedOTPEmail(
        subject=presentation.subject_template,
        body_text=body_text,
        body_html=body_html,
    )
