from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.auth_exceptions import InvalidCredentialsError
from app.domain.exceptions.user_exceptions import UserNotFoundError
from app.domain.models import VerificationToken
from app.domain.services.email_service import EmailService
from app.infrastructure.repositories import EmailVerifTokenRepo, UserRepo


class EmailVerificationService:
    """Service for handling email verification functionality."""

    def __init__(self, session: AsyncSession):
        self.session = session

        # Initialize repositories
        self.user_repo = UserRepo(session)
        self.verif_token_repo = EmailVerifTokenRepo(session)

        # Initialize services
        self.email_service = EmailService()

    async def verify_email(self, *, token: str) -> None:
        """Verify user email using a valid token."""

        hashed_token = VerificationToken.get_hash(token)

        async with self.session.begin():
            verif_token_orm = await self.verif_token_repo.get_by_token(hashed_token=hashed_token)
            if not verif_token_orm:
                raise InvalidCredentialsError()

            VerificationToken.from_orm(verif_token_orm).verify()

            await self.verif_token_repo.delete_by_user_id(user_id=verif_token_orm.user_id)
            await self.user_repo.verify_email(user_id=verif_token_orm.user_id)

    async def resend_verification_email(self, *, email: str) -> None:
        """Resend verification email to the user."""

        async with self.session.begin():
            user_orm = await self.user_repo.get_by_email(email=email)
            if not user_orm:
                raise UserNotFoundError()

            verif_token = VerificationToken.create(user_id=user_orm.id)
            user_email = user_orm.email

            await self.verif_token_repo.delete_by_user_id(user_id=user_orm.id)
            await self.verif_token_repo.add(verif_token=verif_token.to_orm())

        self.email_service.send_verification_email(
            email_to=user_email,
            token=verif_token.token,
        )
