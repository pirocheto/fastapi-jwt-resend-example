import pytest
from httpx import AsyncClient

from tests.factories import PasswordResetTokenFactory, UserFactory
from tests.utils import fake

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
]


async def test_reset_password_success(
    client: AsyncClient,
    reset_token_factory: PasswordResetTokenFactory,
    user_factory: UserFactory,
) -> None:
    new_password = fake.password()

    # Create a user and a reset token for that user
    user = await user_factory.create()
    reset_token = await reset_token_factory.create(user_id=user.id)

    data = {"token": reset_token.token, "new_password": new_password}
    response = await client.post("/api/auth/reset-password", json=data)
    assert response.status_code == 204
