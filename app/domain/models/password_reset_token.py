import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.exceptions.auth_exceptions import InvalidRefreshTokenError
from app.domain.models.base import DomainModel
from app.infrastructure.db.models import PasswordResetTokenORM, default_password_reset_token_expires_at
from app.infrastructure.security import hashing, tokens
from app.mappers import mapper


@dataclass
class PasswordResetToken(DomainModel):
    """Domain model for a password reset token."""

    hashed_token: str
    user_id: uuid.UUID
    _token: str | None = field(default=None, repr=False)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    expired_at: datetime = field(default_factory=lambda: default_password_reset_token_expires_at())
    updated_at: datetime | None = field(default=None)

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
        if self.expired_at < datetime.now(UTC):
            raise InvalidRefreshTokenError()
        return self

    def to_orm(self) -> "PasswordResetTokenORM":
        """Convert the domain model to an ORM model."""
        return mapper.domain_to_orm(self, PasswordResetTokenORM)

    @classmethod
    def from_orm(cls, orm_obj: PasswordResetTokenORM) -> "PasswordResetToken":
        """Convert an ORM model to the domain model."""
        return mapper.orm_to_domain(orm_obj, cls)
