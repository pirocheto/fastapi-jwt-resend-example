from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.auth_exceptions import (
    InvalidPasswordResetTokenError,
)
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
)
from app.domain.models import PasswordResetToken
from app.domain.services.email_service import EmailService
from app.infrastructure.repositories import PasswordResetTokenRepo, UserRepo
from app.infrastructure.security import hashing


class PasswordService:
    """Service for handling password reset functionality."""

    def __init__(self, session: AsyncSession):
        self.session = session

        # Initialize repositories
        self.user_repo = UserRepo(session)
        self.reset_token_repo = PasswordResetTokenRepo(session)

        # Initalize services
        self.email_service = EmailService()

    async def forgot_password(self, *, email: str) -> None:
        """Request a password reset link for the user."""

        async with self.session.begin():
            user_orm = await self.user_repo.get_by_email(email=email)

            if not user_orm:
                raise UserNotFoundError()

            password_reset_token = PasswordResetToken.create(user_id=user_orm.id)
            user_email = user_orm.email

            await self.reset_token_repo.delete_by_user_id(user_id=user_orm.id)
            await self.reset_token_repo.add(reset_token=password_reset_token.to_orm())

        self.email_service.send_password_reset_email(
            email_to=user_email,
            token=password_reset_token.token,
        )

    async def reset_password(self, *, token: str, new_password: str) -> None:
        """Reset user password using a valid token."""

        hashed_token = PasswordResetToken.get_hash(token)
        new_hashed_password = hashing.get_password_hash(new_password)

        async with self.session.begin():
            reset_token_orm = await self.reset_token_repo.get_by_token(hashed_token=hashed_token)

            if not reset_token_orm:
                raise InvalidPasswordResetTokenError()

            PasswordResetToken.from_orm(reset_token_orm).verify()

            await self.reset_token_repo.delete_by_user_id(user_id=reset_token_orm.user_id)
            await self.user_repo.update_password(
                user_id=reset_token_orm.user_id,
                hashed_password=new_hashed_password,
            )
