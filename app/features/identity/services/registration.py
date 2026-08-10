"""
app/features/identity/services/registration.py

Registration related code fun and so on will be present here
"""

from app.shared.otp.enums import (
    OTPPurpose,
    OTPSendStatus,
)

from ..domain.email_validation import ValidatedEmail
from ..exceptions import InvalidEmailError

from ..enums import (
    AfterRegistrationNextStep,
    RegistrationOTPStatus,
    RegistrationStatus,
)

from ..models import (
    RegistrationResult,
    RegistrationViaOTPResult,
)

from .otp import send_otp_to_email, verify_otp_against_email
from ..repository.user import UserRepository


class RegistrationService:
    """
    This will have all the registration related things
    fucntion and checking form this
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    def start_registration(
        self,
        email: str,
    ) -> RegistrationResult:
        """
        It need to send otp in background and send response to user
        quickly i will do this later

        Raise:
            InvalidEmailError

        #TODO
        """

        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value

        except InvalidEmailError:
            raise

        existing_user = self._user_repository.exists_by_email(
            email=validated_email_id,
        )
        if existing_user:
            x = RegistrationResult(
                status=RegistrationStatus.EMAIL_ALREADY_REGISTERED,
                next_step=AfterRegistrationNextStep.ENTER_PASSWORD,
            )
            return x

        # Here i need to check if the email is already register or not
        # and based on this i will send him register email else i will
        # send him the page to login with password or with otp as my
        # business logic will say to do this

        # database checking function will run here

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
            )
            return x

        elif otp_send.status == OTPSendStatus.COOLDOWN_ACTIVE:
            return RegistrationResult(
                status=RegistrationStatus.OTP_COOLDOWN_ACTIVE,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
            )

        elif otp_send.status == OTPSendStatus.EMAIL_BLOCKED:
            return RegistrationResult(
                status=RegistrationStatus.EMAIL_BLOCKED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
            )

        elif otp_send.status == OTPSendStatus.ATTEMPT_LIMIT_EXCEEDED:
            return RegistrationResult(
                status=RegistrationStatus.ATTEMPT_LIMIT_EXCEED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
            )

        elif otp_send.status in (
            OTPSendStatus.SEND_FAILED,
            OTPSendStatus.EMAIL_SERVER_FAILED,
        ):
            return RegistrationResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
            )

        else:
            x = RegistrationResult(
                status=RegistrationStatus.EMAIL_SERVICE_FAILED,
                next_step=AfterRegistrationNextStep.SHOW_ERROR,
            )

            return x

    def verify_registration_otp(
        self,
        email: str,
        submitted_otp: str,
    ) -> RegistrationViaOTPResult:
        """
        This will verify the otp given by user at verify otp case
        """
        # as i cannot depends on the email id data i got from the sesion
        # i will again check the validaiton of the email
        try:
            validated_email_id = ValidatedEmail(
                email_id=email,
            ).value

        except InvalidEmailError:
            raise

        verify = verify_otp_against_email(
            email=validated_email_id,
            purpose=OTPPurpose.REGISTER,
            submitted_otp=submitted_otp,
        )

        if verify.success:

            return RegistrationViaOTPResult(
                status=RegistrationOTPStatus.VERIFIED,
            )

        return RegistrationViaOTPResult(
            status=RegistrationOTPStatus.INVALID_OTP,
        )
