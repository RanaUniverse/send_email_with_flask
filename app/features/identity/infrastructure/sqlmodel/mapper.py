"""
app/features/identity/infrastructure/sqlmodel/mapper.py

This is for convert my models to business need like this
"""

from ...domain.entities.user import UserDomain

from .models import UserOutForDomainEntity, UserModel


def to_domain(
    model_obj: UserOutForDomainEntity,
) -> UserDomain:
    """
    from the sqlmodel database user to my business entities
    userclass i will make here
    """

    obj = UserDomain(
        id_=model_obj.id_,
        email=model_obj.email,
        hashed_password=model_obj.hashed_password,
        is_active=model_obj.is_active,
        is_verified=model_obj.is_verified,
    )

    return obj


def to_model(user_obj: UserDomain) -> UserModel:
    """
    get the entity user obj and make this to be in sqlmodle table
    data to use
    """
    obj = UserModel.model_validate(user_obj)
    return obj
