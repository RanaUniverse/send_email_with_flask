"""
app/shared/security/otp_templates.py

I will generate the template of html
"""


def otp_email_body(
    otp: str,
    valid_seconds: int = 60,
) -> str:
    return (
        "Hello,\n\n"
        f"Your verification code is: {otp}\n\n"
        f"This code is valid for {valid_seconds} seconds.\n\n"
        "If you didn't request this code, you can ignore this email."
    )
