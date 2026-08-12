"""
app/features/identity/forms.py

Here i will defines the class for my flask_wtf forms
"""

from flask_wtf import (  # type: ignore
    FlaskForm,
)

from wtforms import (
    PasswordField,
    SubmitField,
    StringField,
    EmailField,
)

from wtforms.validators import DataRequired, Length, Email


class EmailMixin:
    email = EmailField(
        label="Email ID",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
            ),
            Email(),
        ],
    )
    # i use below sometime to check if frontend fails to email id check i will
    # check with below valud if my backend will do it properly

    # email = StringField(
    #     label="Email ID",
    #     validators=[
    #         DataRequired(),
    #         Length(
    #             min=1,
    #             max=50,
    #         ),
    #     ],
    # )


class LoginForm(FlaskForm, EmailMixin):

    password = PasswordField(
        label="Enter Your Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField(
        label="Login Now",
    )


class RegisterForm(FlaskForm, EmailMixin):
    submit = SubmitField(
        label="Register New Account",
    )


class OTPForm(FlaskForm):
    otp = StringField(
        label="Enter OTP",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=10,
            ),
        ],
    )
    # for now i  keep this 4 to 10 so that later i will change this
    submit = SubmitField(
        label="Verify Your OTP",
    )
