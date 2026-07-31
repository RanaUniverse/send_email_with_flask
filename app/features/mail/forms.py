"""
app/features/mail/forms.py

Email sending form will be here
"""

from flask_wtf import FlaskForm  # type: ignore

from wtforms import EmailField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length


# This below will be in core.py in forms section as this
# will need by both only otp send and also for email send
class EmailToForm:
    email = EmailField(
        label="Recipient(Example: my_name@gmail.com)",
        validators=[DataRequired(), Email()],
    )


class OtpEmailForm(
    EmailToForm,
    FlaskForm,
):
    submit = SubmitField(
        label="Request For OTP",
    )


class SendEmailForm(
    EmailToForm,
    FlaskForm,
):
    subject = StringField(
        label="Subject(Max 40 Letters)",
        validators=[DataRequired(), Length(min=3, max=40)],
    )

    body = TextAreaField(
        label="Message(Max 4000 Letters)",
        validators=[DataRequired(), Length(min=3, max=4000)],
    )

    submit = SubmitField(
        label="Send The Mail",
    )
