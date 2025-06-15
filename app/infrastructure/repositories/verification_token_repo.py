import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import VerificationTokenORM


class EmailVerifTokenRepo:
    """Repository for refresh token-related database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, *, verif_token: VerificationTokenORM) -> None:
        """Add a new verification token to the database."""

        self.session.add(verif_token)

    async def delete_by_user_id(self, *, user_id: uuid.UUID) -> None:
        """Delete all refresh tokens associated with a user ID."""

        statement = delete(VerificationTokenORM).where(VerificationTokenORM.user_id == user_id)
        await self.session.execute(statement)

    async def get_by_token(self, *, hashed_token: str) -> VerificationTokenORM | None:
        """Retrieve a verification token by its token string."""

        statement = select(VerificationTokenORM).where(VerificationTokenORM.hashed_token == hashed_token)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
