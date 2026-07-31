"""
app/features/mail/service.py

Here i will keep the business logic of what to do
or what to validate or not i will call the operations.py
"""

from pydantic import EmailStr


from app.shared.email.models import EmailMessageData

from app.shared.email.sender import EmailSender
from app.shared.email.factory import mail_sender


class MailService:
    def __init__(
        self,
        sender: EmailSender,
    ) -> None:
        self.sender = sender

    def send_otp(
        self,
        to_email: EmailStr,
    ):
        # this otp generate will be done in another fun
        random_otp = 123456
        msg_body = (
            f"Hello User, your otp for veification is: {random_otp}, "
            "valid for 60 seconds."
        )

        mail_data = EmailMessageData(
            to_email=[to_email, "x@co.m"],
            subject="OTP SENDING",
            body=msg_body,
        )
        self.sender.send_mail(
            email_msg=mail_data,
        )


def send_otp_to_email(to_email: str):
    m = MailService(
        sender=mail_sender,
    )
    m.send_otp(
        to_email=to_email,
    )


# def send_otp_to_email_old(
#     to_email: str,
# ):
#     """
#     This is my business logic this fun will call in the routes.py
#     here i will deceide what protocle and what msg i will send
#     and how i will do it by the email sending way

#     Now this is generating otp, msg body later i will separate this in
#     differnet module and just call the sender.send_mail
#     """

#     # it will create a random secret number in reality
#     otp = 123456

#     msg_body = f"Hello User, your otp for veification is: {otp}, valid for 60 seconds."

#     mail_data = EmailMessageData(
#         to_email=[to_email, "x@co.m"],
#         subject="OTP SENDING",
#         body=msg_body,
#     )
#     # below will some logic to from where the mail will send
#     # mail_data.from_email = "user_own@gmail.com"

#     local = LocalMailSender(
#         local_config=local_config,
#     )
#     local.send_mail(
#         email_msg=mail_data,
#     )

#     # gmail = GmailSender(
#     #     gmail_config=gmail_config,
#     # )
#     # gmail.send_mail(
#     #     email_msg=mail_data,
#     # )


def send_email_to_one_user():
    """
    This will just Send the mail to the user or whatsoever
    This is my business logic,
    here it will choose if the mail will go over gmail, local or anything else
    """
    pass
