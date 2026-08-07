"""
app/shared/otp/render.py

This is responsible to generate the structer of how the mail
data or message will shows to the user.
"""

from flask import render_template


def render_login_otp(
    *,
    otp: str,
    valid_seconds: int,
) -> tuple[str, str]:
    # The body will come form the Root Level templates html file
    body_text = render_template(
        template_name_or_list="emails/otp/login.txt",
        otp=otp,
        valid_seconds=valid_seconds,
    )
    body_html = render_template(
        template_name_or_list="emails/otp/login.html",
        otp=otp,
        valid_seconds=valid_seconds,
    )
    return body_text, body_html


if __name__ == "__main__":
    print(render_login_otp(otp="446666", valid_seconds=3))
