from fastapi import status

from app.domain.exceptions.base_exceptions import AppError


class InvalidAccessTokenError(AppError):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_access_token",
            detail="Access token is invalid or expired",
        )


class InvalidVerificationTokenError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="invalid_verification_token",
            detail="Verification token is invalid or expired",
        )


class RefreshTokenExpiredError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="refresh_token_expired",
            detail="Refresh token has expired",
        )


class IncorrectPasswordError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="incorrect_password",
            detail="The provided password is incorrect",
        )


class UserNotVerifiedError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="user_not_verified",
            detail="User account is not verified",
        )


class InvalidCredentialsError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_credentials",
            detail="Invalid email or password",
        )


class InvalidRefreshTokenError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="invalid_refresh_token",
            detail="Refresh token is invalid or expired",
        )


class InvalidPasswordResetTokenError(AppError):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="invalid_password_reset_token",
            detail="Password reset token is invalid or expired",
        )
