import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.exceptions.auth_exceptions import IncorrectPasswordError, InvalidCredentialsError, UserNotVerifiedError
from app.domain.models.base import DomainModel
from app.infrastructure.db.models import UserORM
from app.infrastructure.mappers import mapper, sync
from app.infrastructure.security import hashing


@dataclass
class User(DomainModel):
    """Domain model for a user."""

    email: str
    hashed_password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    is_verified: bool = False

    def verify_can_login(self) -> "User":
        """Verify if the user can log in."""

        if not self.is_verified:
            raise UserNotVerifiedError()
        return self

    def verify_password(self, password: str) -> "User":
        """Verify the user's password."""

        if not hashing.verify_password(password, self.hashed_password):
            raise IncorrectPasswordError()
        return self

    def authenticate(self, password: str) -> "User":
        """Authenticate the user with the provided password."""

        try:
            self.verify_can_login()
            self.verify_password(password)
        except (UserNotVerifiedError, IncorrectPasswordError):
            raise InvalidCredentialsError()
        return self

    @classmethod
    def create(cls, email: str, password: str, is_verified: bool = False) -> "User":
        """Create a new user instance."""

        hashed_password = hashing.get_password_hash(password)
        return cls(email=email, hashed_password=hashed_password, is_verified=is_verified)

    def to_orm(self) -> UserORM:
        """Convert the domain model to an ORM model."""

        return mapper.domain_to_orm(self, UserORM)

    @classmethod
    def from_orm(cls, obj_orm: UserORM) -> "User":
        """Create a domain model from an ORM model."""

        return mapper.orm_to_domain(obj_orm, cls)

    def sync(self, orm_obj: UserORM) -> "User":
        """Synchronize the domain model with the ORM model."""
        return sync.domain_from_orm(self, orm_obj)
