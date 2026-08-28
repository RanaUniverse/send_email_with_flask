"""
app/features/identity/infrastructure/sqlmodel/user_repository.py

The implementation:
   "How do I actually query PostgreSQL/SQLite/MongoDB?"

for the sqlmodel i will write code here

"""

# i am using the below class as a protocol to make this below
# from ...domain.repositories.user_repository import UserRepository

from ...domain.entities.user import UserDomain


from sqlmodel import Session, select

from .mapper import to_domain, to_model
from .models import UserModel


class SQLModelUserRepository:
    def __init__(
        self,
        session: Session,
    ) -> None:
        pass

    def get_by_id(self, user_id: str) -> UserDomain | None: ...

    def get_by_email(self, email: str) -> UserDomain | None: ...

    def exists_by_email(self, email: str) -> bool: ...

    def add(self, user: UserDomain) -> UserDomain: ...

    def update(self, user: UserDomain) -> UserDomain: ...
