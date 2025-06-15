import pytest
from httpx import AsyncClient

from tests.factories import UserFactory, VerificationTokenFactory

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
]


async def test_verify_email_success(
    client: AsyncClient, user_factory: UserFactory, verif_token_factory: VerificationTokenFactory
) -> None:
    user = await user_factory.create()
    verif_token = await verif_token_factory.create(user.id)

    response = await client.post("/api/auth/verify-email", json={"token": verif_token.token})
    assert response.status_code == 204
