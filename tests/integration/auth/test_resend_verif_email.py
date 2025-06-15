import pytest
from httpx import AsyncClient

from tests.factories import UserFactory

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.integration,
]


async def test_resend_verif_email_success(client: AsyncClient, user_factory: UserFactory) -> None:
    user = await user_factory.create(is_verified=False)
    response = await client.post("api/auth/resend-verification", json={"email": user.email})
    assert response.status_code == 204
