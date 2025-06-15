import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.auth_exceptions import InvalidAccessTokenError
from app.domain.exceptions.user_exceptions import UserNotFoundError
from app.domain.models import AccessToken, User
from app.infrastructure.repositories import UserRepo


class UserService:
    """Service for handling user-related functionality."""

    def __init__(self, session: AsyncSession):
        self.session = session

        # Initialize repositories
        self.user_repo = UserRepo(session)

    async def get_user_by_access_token(self, access_token: str) -> User:
        """Retrieve a user by access token."""

        token = AccessToken.from_token(access_token)
        if not token:
            raise InvalidAccessTokenError()

        return await self.get_user_by_id(token.user_id)

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        """Retrieve a user by ID."""

        user_orm = await self.user_repo.get_by_id(user_id=user_id)
        if not user_orm:
            raise UserNotFoundError()

        return User.from_orm(user_orm)
