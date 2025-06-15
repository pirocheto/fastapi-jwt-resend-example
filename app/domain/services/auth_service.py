from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions.auth_exceptions import (
    InvalidCredentialsError,
    InvalidRefreshTokenError,
)
from app.domain.models import AccessToken, RefreshToken, User
from app.infrastructure.repositories import RefreshTokenRepo, UserRepo
from app.schemas.auth import TokenPair


class AuthService:
    """Service for handling user authentication functionality."""

    def __init__(self, session: AsyncSession):
        self.session = session

        # Initialize repositories
        self.user_repo = UserRepo(session)
        self.refresh_token_repo = RefreshTokenRepo(session)

    async def login_user(self, *, email: str, password: str) -> TokenPair:
        """Authenticate user and return access and refresh tokens."""

        async with self.session.begin():
            user_orm = await self.user_repo.get_by_email(email=email)

            if not user_orm:
                raise InvalidCredentialsError()

            user = User.from_orm(user_orm).authenticate(password)

            refresh_token = RefreshToken.create(user_id=user.id)
            access_token = AccessToken.create(user_id=user.id)

            await self.refresh_token_repo.delete_by_user_id(user_id=user.id)
            await self.refresh_token_repo.add(refresh_token=refresh_token.to_orm())

        return TokenPair(access_token=access_token.token, refresh_token=refresh_token.token)

    async def refresh_access_token(self, *, refresh_token: str) -> TokenPair:
        """Refresh the access token using a valid refresh token."""

        hashed_refresh_token = RefreshToken.get_hash(refresh_token)

        async with self.session.begin():
            refresh_token_orm = await self.refresh_token_repo.get_by_token(hashed_refresh_token)

            if not refresh_token_orm:
                raise InvalidRefreshTokenError()

            RefreshToken.from_orm(refresh_token_orm).verify()

            new_refresh_token = RefreshToken.create(user_id=refresh_token_orm.user_id)
            access_token = AccessToken.create(user_id=refresh_token_orm.user_id)

            await self.refresh_token_repo.delete_by_user_id(refresh_token_orm.user_id)
            await self.refresh_token_repo.add(new_refresh_token.to_orm())

        return TokenPair(access_token=access_token.token, refresh_token=new_refresh_token.token)
