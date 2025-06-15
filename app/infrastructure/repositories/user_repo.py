import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import UserORM, VerificationTokenORM


class UserRepo:
    """Repository for user-related database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, *, email: str) -> UserORM | None:
        """Retrieve a user by email."""

        statement = select(UserORM).where(UserORM.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_id(self, *, user_id: uuid.UUID) -> UserORM | None:
        """Retrieve a user by ID."""

        statement = select(UserORM).where(UserORM.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, *, user: UserORM) -> None:
        """Add a new user to the database."""

        self.session.add(user)

    async def delete_token_by_user_id(self, *, user_id: uuid.UUID) -> None:
        """Delete all refresh tokens associated with a user ID."""

        statement = delete(VerificationTokenORM).where(VerificationTokenORM.user_id == user_id)
        await self.session.execute(statement)

    async def update_password(self, *, user_id: uuid.UUID, hashed_password: str) -> None:
        """Update the password for a user."""

        statement = update(UserORM).where(UserORM.id == user_id).values(hashed_password=hashed_password)
        await self.session.execute(statement)

    async def verify_email(self, *, user_id: uuid.UUID) -> None:
        """Verify a user by setting the verified flag to True."""

        statement = update(UserORM).where(UserORM.id == user_id).values(is_verified=True)
        await self.session.execute(statement)
