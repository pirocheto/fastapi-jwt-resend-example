from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.user_exceptions import (
    UserAlreadyExistsError,
)
from app.domain.models import User, VerificationToken
from app.domain.services.email_service import EmailService
from app.infrastructure.repositories import EmailVerifTokenRepo, UserRepo


class RegistrationService:
    """Service for handling user registration functionality."""

    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepo(session)
        self.verif_token_repo = EmailVerifTokenRepo(session)

        # Initialize services
        self.email_service = EmailService()

    async def register_user(self, email: str, password: str) -> User:
        """Register a new user and send verification email."""

        existing_user = await self.user_repo.get_by_email(email=email)
        if existing_user:
            raise UserAlreadyExistsError()

        user = User.create(email=email, password=password)
        verif_token = VerificationToken.create(user_id=user.id)

        await self.user_repo.add(user=user.to_orm())
        await self.verif_token_repo.add(verif_token=verif_token.to_orm())

        self.email_service.send_verification_email(email_to=user.email, token=verif_token.token)
        return user
