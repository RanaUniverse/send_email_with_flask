"""
app/features/identity/services.py

Here i will write my business logics like how the login works and so on
"""

from pydantic import EmailStr


from ..domain.email_validation import ValidatedEmail
from ..exceptions import InvalidEmailError
from ..user import USER_, User


from .otp import send_register_otp_to_email

from ..enums import RegistrationStatus, AfterRegistrationNextStep
from ..models import RegistrationResult

from app.shared.otp.models import OTPSendStatus


from ..user import USER_, User


class UserRepository:
    """
    This is have user related information extract methods
    """

    def get_by_email(
        self,
        email: EmailStr,
    ) -> User | None:

        for user in USER_.values():
            if user.email == email:
                return user

        return None

    def exists_by_email(
        self,
        email: EmailStr,
    ) -> bool:

        return self.get_by_email(email) is not None


def check_authentication(
    email: EmailStr,
    password: str,
) -> User | None:
    """
    Authenticate a user using an email address and password.

    Returns:
        User: The authenticated user if the credentials are valid.
        None: If authentication fails.
    """
    u = UserRepository()
    user_obj = u.get_by_email(
        email=email,
    )
    if not user_obj:
        return None

    stored_password = user_obj.password

    if password == stored_password:
        return user_obj


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

        otp_send = send_register_otp_to_email(
            email_id=validated_email_id,
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


user_repository_obj = UserRepository()
registration_service_obj = RegistrationService(
    user_repository=user_repository_obj,
)
