import uuid
from dataclasses import dataclass
from typing import Any

from app.domain.exceptions.auth_exceptions import InvalidAccessTokenError
from app.domain.models.base import DomainModel
from app.infrastructure.security import tokens


@dataclass
class AccessToken(DomainModel):
    """Domain model for an access token."""

    token: str
    user_id: uuid.UUID
    payload: dict[str, Any]

    @classmethod
    def create(cls, user_id: uuid.UUID) -> "AccessToken":
        """Create a new access token for a user."""

        payload = tokens.create_jwt_payload(subject=user_id)
        token = tokens.encode_jwt_token(payload)
        return cls(token=token, user_id=user_id, payload=payload)

    @classmethod
    def from_token(cls, token: str) -> "AccessToken":
        """Create an AccessToken instance from a token string."""

        payload = tokens.decode_jwt_token(token)
        if payload is None or "sub" not in payload:
            raise InvalidAccessTokenError()
        user_id = uuid.UUID(payload["sub"])
        return cls(token=token, user_id=user_id, payload=payload)
