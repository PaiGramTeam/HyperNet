from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from hypernet.client.components.auth import AuthClient
from hypernet.utils.enums import Region

if TYPE_CHECKING:
    from hypernet.client.cookies import Cookies


@pytest_asyncio.fixture
async def auth_client(region: "Region", cookies: "Cookies"):
    async with AuthClient(
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestAuthClient:
    @staticmethod
    async def test_get_account_info_by_hg_token(auth_client: "AuthClient"):
        account_info = await auth_client.get_account_info_by_hg_token()
        assert account_info is not None
        assert account_info.hgId == auth_client.hg_id

    @staticmethod
    async def test_refresh_sign_token(auth_client: "AuthClient"):
        resp = await auth_client.get_sign_token()
        assert resp is not None
