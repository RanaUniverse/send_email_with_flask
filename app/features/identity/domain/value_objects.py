"""
app/features/identity/domain/value_objects.py

Here i will make some checking of thigns related to this domain
"""

from pydantic import BaseModel, EmailStr, field_validator


from ..exceptions import InvalidEmailError


class EmailModel(BaseModel):
    value: EmailStr

    @field_validator("value")
    @classmethod
    def allowed_providers(cls, email: EmailStr):
        allowed_domains = {
            "gmail.com",
            "hotmail.com",
            "outlook.com",
            "yahoo.com",
        }

        domain = str(email).split("@")[-1].lower()

        if domain not in allowed_domains:
            raise InvalidEmailError(
                "Only Trusted Gmail, Hotmail, Outlook, and Yahoo emails are allowed. Else Contact Support."
            )

        return email
