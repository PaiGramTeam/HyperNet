from typing import TYPE_CHECKING, Optional

import pytest
import pytest_asyncio

from hypernet.client.components.auth import AuthClient
from hypernet.errors import RedemptionInvalid, RedemptionClaimed
from hypernet.utils.enums import Region

if TYPE_CHECKING:
    from hypernet.client.cookies import Cookies

    from hypernet.models.lab.game_role import GameRoleId


@pytest_asyncio.fixture
async def auth_client(region: "Region", cookies: "Cookies"):
    async with AuthClient(
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


BINDING_TOKEN = ""
BINDING_ROLE_ID: Optional["GameRoleId"] = None
BINDING_ROLE_TOKEN = ""


@pytest.mark.asyncio
class TestAuthClient:
    @staticmethod
    async def test_a_get_game_accounts_by_binding_token(auth_client: "AuthClient"):
        global BINDING_TOKEN
        BINDING_TOKEN = token = await auth_client.get_binding_token_by_hg_token()
        assert token is not None

    @staticmethod
    async def test_b_get_role_id_by_player_id(auth_client: "AuthClient", endfield_player_id: int):
        global BINDING_ROLE_ID
        BINDING_ROLE_ID = role_id = await auth_client.get_role_id_by_player_id(BINDING_TOKEN, endfield_player_id)
        assert role_id is not None

    @staticmethod
    async def test_c_get_role_token_by_binding_token(auth_client: "AuthClient"):
        global BINDING_ROLE_TOKEN
        BINDING_ROLE_TOKEN = role_token = await auth_client.get_role_token_by_binding_token(
            BINDING_TOKEN,
            BINDING_ROLE_ID.role_id,
        )
        assert role_token is not None

    @staticmethod
    @pytest.mark.xfail(raises=RedemptionInvalid, reason="Invalid gift code used for testing.")
    async def test_d_redeem_gift_code_by_role_token_invalid(auth_client: "AuthClient"):
        resp = await auth_client.redeem_gift_code_by_role_token(
            "abc123",
            BINDING_ROLE_TOKEN,
            server_id=BINDING_ROLE_ID.server_id,
            channel_id=BINDING_ROLE_ID.channel_id,
        )
        assert resp is not None

    @staticmethod
    @pytest.mark.xfail(raises=RedemptionClaimed, reason="Gift code already claimed used for testing.")
    async def test_d_redeem_gift_code_by_role_token_already(auth_client: "AuthClient"):
        resp = await auth_client.redeem_gift_code_by_role_token(
            "ALLFIELD",
            BINDING_ROLE_TOKEN,
            server_id=BINDING_ROLE_ID.server_id,
            channel_id=BINDING_ROLE_ID.channel_id,
        )
        assert resp is not None

    @staticmethod
    async def test_get_account_info_by_hg_token(auth_client: "AuthClient"):
        account_info = await auth_client.get_account_info_by_hg_token()
        assert account_info is not None
        assert account_info.hgId == auth_client.hg_id

    @staticmethod
    async def test_refresh_sign_token(auth_client: "AuthClient"):
        resp = await auth_client.get_sign_token()
        assert resp is not None
