import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.config import settings
from app.domain.exceptions.auth_exceptions import InvalidRefreshTokenError
from app.domain.models.base import DomainModel
from app.infrastructure.db.models import PasswordResetTokenORM
from app.infrastructure.mappers import mapper, sync
from app.infrastructure.security import hashing, tokens


def default_password_reset_token_expires_at() -> datetime:
    """Default expiration time for password reset tokens."""
    return datetime.now(UTC) + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS)


@dataclass
class PasswordResetToken(DomainModel):
    """Domain model for a password reset token."""

    hashed_token: str
    user_id: uuid.UUID
    _token: str | None = field(default=None, repr=False)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime = field(default_factory=lambda: default_password_reset_token_expires_at())

    @property
    def token(self) -> str:
        if self._token is None:
            raise RuntimeError("Token is not available (likely loaded from DB)")
        return self._token

    @classmethod
    def create(cls, user_id: uuid.UUID) -> "PasswordResetToken":
        """Create a new password reset token for a user."""

        opaque_token = tokens.create_opaque_token()
        return cls.from_token(token=opaque_token, user_id=user_id)

    @classmethod
    def from_token(cls, token: str, user_id: uuid.UUID) -> "PasswordResetToken":
        """Create a new password reset token from an token."""

        hashed_token = hashing.get_token_hash(token)
        return cls(
            user_id=user_id,
            _token=token,
            hashed_token=hashed_token,
        )

    @staticmethod
    def get_hash(token: str) -> str:
        """Get the hashed value of the token."""
        return hashing.get_token_hash(token)

    def verify(self) -> "PasswordResetToken":
        """Verify the integrity of the password reset token."""
        if self.expires_at < datetime.now(UTC):
            raise InvalidRefreshTokenError()
        return self

    def to_orm(self) -> "PasswordResetTokenORM":
        """Convert the domain model to an ORM model."""
        return mapper.domain_to_orm(self, PasswordResetTokenORM)

    @classmethod
    def from_orm(cls, orm_obj: PasswordResetTokenORM) -> "PasswordResetToken":
        """Convert an ORM model to the domain model."""
        return mapper.orm_to_domain(orm_obj, cls)

    def sync(self, orm_obj: PasswordResetTokenORM) -> "PasswordResetToken":
        """Synchronize the domain model with the ORM model."""
        return sync.domain_from_orm(self, orm_obj)
