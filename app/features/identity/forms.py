"""
app/features/identity/forms.py

Here i will defines the class for my flask_wtf forms
"""

from flask_wtf import (  # type: ignore
    FlaskForm,
)

from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
)

from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField(
        label="Email ID",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=50,
            ),
        ],
    )

    password = PasswordField(
        label="Enter Your Password",
        validators=[
            DataRequired(),
        ],
    )

    submit = SubmitField(
        label="Login Now",
    )


class RegisterForm(FlaskForm):
    """
    # TODO
    I will make this later
    """

    ...
