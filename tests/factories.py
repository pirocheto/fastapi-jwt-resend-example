import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.user_exceptions import UserAlreadyExistsError
from app.domain.models import PasswordResetToken, User, VerificationToken
from app.infrastructure.repositories import UserRepo
from tests.utils import fake


class UserFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepo(session)

    async def create(
        self,
        email: str | None = None,
        password: str | None = None,
        is_verified: bool = True,
        commit: bool = True,
    ) -> User:
        """
        Create a user with the given parameters.
        If commit is True, the user will be added to the session and committed.
        """
        if email:
            existing_user = await self.user_repo.get_by_email(email=email)
            if existing_user:
                raise UserAlreadyExistsError()

        user = User.create(
            email=email or fake.email(),
            password=password or fake.password(),
            is_verified=is_verified,
        )

        await self.user_repo.add(user=user.to_orm())

        if commit:
            try:
                await self.session.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                await self.session.rollback()
                raise UserAlreadyExistsError()
        return user


class PasswordResetTokenFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: uuid.UUID, commit: bool = True) -> PasswordResetToken:
        """
        Create a password reset token for the given user.
        If commit is True, the token will be added to the session and committed.
        """
        password_reset_token = PasswordResetToken.create(user_id=user_id)

        if commit:
            self.session.add(password_reset_token.to_orm())
            await self.session.commit()

        return password_reset_token


class VerificationTokenFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: uuid.UUID, commit: bool = True) -> VerificationToken:
        """
        Create a verification token for the given user.
        If commit is True, the token will be added to the session and committed.
        """
        verification_token = VerificationToken.create(user_id=user_id)

        if commit:
            self.session.add(verification_token.to_orm())
            await self.session.commit()

        return verification_token
