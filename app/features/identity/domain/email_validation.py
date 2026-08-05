"""
app/features/identity/domain/email_validation.py

Here my email validaion will logic stays so that my service dont
know how the validiaon works and which way?
"""

from pydantic import EmailStr, ValidationError

from .value_objects import EmailModel

from ..exceptions import InvalidEmailError


class ValidatedEmail:
    """
    It can reaise InvalidEmailError from exceptions.py
    """

    def __init__(
        self,
        email_id: str,
    ) -> None:
        try:
            model = EmailModel(
                value=email_id,
            )

        except InvalidEmailError:
            raise

        except ValidationError:
            raise InvalidEmailError(
                "Please Use Your Proper Email ID",
            )
        self._value = model.value

    @property
    def value(self) -> EmailStr:
        email_str = self._value
        return email_str
