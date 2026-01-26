from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from hypernet.client.components.lab import LabClient

if TYPE_CHECKING:
    from hypernet.client.cookies import Cookies
    from hypernet.utils.enums import Region


@pytest_asyncio.fixture
async def client_instance(region: "Region", cookies: "Cookies"):
    async with LabClient(
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestLabClient:
    @staticmethod
    async def test_check_lab_user(client_instance: "LabClient"):
        user_info = await client_instance.check_lab_user()
        assert user_info is not None
        assert user_info.isNewUser == False
        assert user_info.nickname is not None

    @staticmethod
    async def test_get_lab_show_user_id(client_instance: "LabClient"):
        lab_user_id = await client_instance.get_lab_show_user_id()
        assert lab_user_id is not None
        assert isinstance(lab_user_id, int)

    @staticmethod
    async def test_get_game_accounts(client_instance: "LabClient"):
        game_accounts = await client_instance.get_game_accounts()
        assert len(game_accounts) > 0
