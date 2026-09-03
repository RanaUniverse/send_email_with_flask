"""
app/features/identity/services/registration.py

Registration related code fun and so on will be present here
"""

from pydantic import EmailStr


from app.shared.otp.enums import (
    OTPPurpose,
    OTPSendStatus,
)

from ...domain.value_objects.email_validation import ValidatedEmail
from ...domain.exceptions import InvalidEmailError

from ...domain.enums import (
    AfterRegistrationNextStep,
    RegistrationOTPStatus,
    RegistrationStatus,
)

from .dto import (
    RegistrationResult,
    RegistrationViaOTPResult,
    RegistrationIdentity,
)


from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user import UserDomain

from ..otp.service import send_otp_to_email, verify_otp_against_email


class RegistrationService:
    """
    This will have all the registration related things
    fucntion and checking form this

    The user_repository valeu will come as dependency
    otp_service -> as a di so that it will know how to send
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:

        self._user_repository = user_repository

    def _add_user_to_db(
        self,
        email: EmailStr,
        hashed_password: str | None = None,
    ) -> UserDomain:

        user_obj = UserDomain(
            email=email,
            hashed_password=hashed_password,
        )
        new_user = self._user_repository.add(user_obj)

        return new_user

    def start_registration(
        self,
        email: str,
    ) -> RegistrationResult:
        """
        #TODO
        For now local development i am sending mail directly later
        i will need to switch to celery and say the user that otp has send.

        It need to send otp in background and send response to user
        quickly i will do this later

        Raise:
            InvalidEmailError
        """
        # This email checking is like business logic if email domain is allowed
        # not spammed domain is allowed here liekt his
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            # my routes can handle this error there and say user
            raise
        #  i am passing this object so that my routes can decide to do with this
        identity_obj = RegistrationIdentity(
            email=validated_email_id,
        )

        existing_user = self._user_repository.exists_by_email(
            email=validated_email_id,
        )

        if existing_user:
            x = RegistrationResult(
                status=RegistrationStatus.EMAIL_ALREADY_REGISTERED,
                next_step=AfterRegistrationNextStep.ENTER_PASSWORD,
                identity=identity_obj,
            )
            return x

        # i am calling a fun which call the backend's email send
        otp_send = send_otp_to_email(
            email_id=validated_email_id,
            purpose=OTPPurpose.REGISTER,
        )

        # Below the data from the otp backend is converted to shows
        # in the interface layer of how to do shows the data

        if otp_send.success:
            x = RegistrationResult(
                status=RegistrationStatus.OTP_SENT,
                next_step=AfterRegistrationNextStep.VERIFY_OTP,
                identity=identity_obj,
            )
            return x

        elif otp_send.status == OTPSendStatus.COOLDOWN_ACTIVE:
            return RegistrationResult(
                status=RegistrationStatus.OTP_COOLDOWN_ACTIVE,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status == OTPSendStatus.EMAIL_BLOCKED:
            return RegistrationResult(
                status=RegistrationStatus.EMAIL_BLOCKED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status == OTPSendStatus.ATTEMPT_LIMIT_EXCEEDED:
            return RegistrationResult(
                status=RegistrationStatus.ATTEMPT_LIMIT_EXCEED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        elif otp_send.status in (
            OTPSendStatus.SEND_FAILED,
            OTPSendStatus.EMAIL_SERVER_FAILED,
        ):
            return RegistrationResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

        else:
            x = RegistrationResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
                identity=identity_obj,
            )

            return x

    def complete_registration_with_otp(
        self,
        email: str,
        submitted_otp: str,
    ) -> RegistrationViaOTPResult:
        """
        For success it will insert data into the db
        and then if wrong any then it will raise a error

        Raise:
            InvalidEmailError

        """
        # even though i think this checkin is not need here, as the email in session should
        # has been validated beforehand
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value
        except InvalidEmailError:
            raise

        # here i think to add some logic to check before
        # if user has attempt exceed like this or not
        verify = verify_otp_against_email(
            email=validated_email_id,
            purpose=OTPPurpose.REGISTER,
            submitted_otp=submitted_otp,
        )

        if verify.success:
            new_user = self._add_user_to_db(
                email=validated_email_id,
            )
            return RegistrationViaOTPResult(
                status=RegistrationOTPStatus.VERIFIED,
                user=new_user,
            )

        return RegistrationViaOTPResult(
            status=RegistrationOTPStatus.NOT_VERIFIED,
        )
