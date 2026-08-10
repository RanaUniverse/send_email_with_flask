"""
app/features/identity/dependencies.py

i will keep all the services obj keep here so that later i can import those
in my routes.py as my service logic will hidden here in this obj like this
"""

from .repository.user import UserRepository
from .services.registration import RegistrationService

user_repository_obj = UserRepository()

registration_service_obj = RegistrationService(
    user_repository=user_repository_obj,
)
