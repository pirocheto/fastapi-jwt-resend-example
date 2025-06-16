from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.domain.services.auth_service import AuthService
from app.domain.services.email_verif_service import EmailVerificationService
from app.domain.services.password_service import PasswordService
from app.domain.services.registration_service import RegistrationService
from app.domain.services.user_service import UserService
from app.infrastructure.db.session import get_db

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

CredentialsDep = Annotated[OAuth2PasswordRequestForm, Depends()]

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]

AccessTokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(user_service: "UserServiceDep", access_token: "AccessTokenDep") -> User:
    return await user_service.get_user_by_access_token(access_token=access_token)


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_user_service(session: "AsyncSessionDep") -> UserService:
    return UserService(session=session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_auth_service(session: "AsyncSessionDep") -> AuthService:
    return AuthService(session=session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_registration_service(session: "AsyncSessionDep") -> RegistrationService:
    return RegistrationService(session=session)


RegistrationServiceDep = Annotated[RegistrationService, Depends(get_registration_service)]


async def password_service(session: "AsyncSessionDep") -> PasswordService:
    return PasswordService(session=session)


PasswordServiceDep = Annotated[PasswordService, Depends(password_service)]


async def email_verif_service(session: "AsyncSessionDep") -> EmailVerificationService:
    return EmailVerificationService(session=session)


EmailVerificationServiceDep = Annotated[EmailVerificationService, Depends(email_verif_service)]
