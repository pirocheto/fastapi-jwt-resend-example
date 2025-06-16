import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.config import settings

ALGORITHM = "HS256"


def create_jwt_payload(subject: Any) -> dict[str, Any]:
    """Create a JWT payload with the necessary claims."""
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        # Expiration time
        "exp": expire,
        # Subject of the token, typically a user ID or username
        "sub": str(subject),
        # Not before time, indicating when the token is valid from
        "nbf": now,
        # Issued at time, indicating when the token was created
        "iat": now,
        # JWT ID, a unique identifier for the token
        "jti": str(uuid.uuid4()),
        # Issuer of the token, typically the backend host
        "iss": settings.BACKEND_HOST,
        # Audience of the token, typically the frontend host
        "aud": settings.FRONTEND_HOST,
    }


def encode_jwt_token(payload: dict[str, Any]) -> str:
    """Create a JWT token from the given payload."""
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            issuer=settings.BACKEND_HOST,
            audience=settings.FRONTEND_HOST,
        )
        return dict(decoded_token)
    except (ExpiredSignatureError, InvalidTokenError):
        return None


def create_opaque_token() -> str:
    return secrets.token_urlsafe(64)
