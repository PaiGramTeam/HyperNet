from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from hypernet import Game
from hypernet.client.components.daily import DailyRewardClient
from hypernet.errors import AlreadyClaimed

if TYPE_CHECKING:
    from hypernet.client.cookies import Cookies
    from hypernet.utils.enums import Region


@pytest_asyncio.fixture
async def client_instance(region: "Region", cookies: "Cookies", endfield_player_id: int):
    async with DailyRewardClient(
        cookies=cookies,
        region=region,
    ) as client_instance:
        client_instance.game = Game.ENDFIELD
        client_instance.player_id = endfield_player_id
        yield client_instance


@pytest.mark.asyncio
class TestDailyClient:
    @staticmethod
    async def test_get_reward_info(client_instance: "DailyRewardClient"):
        reward_info = await client_instance.get_reward_info()
        assert reward_info is not None

    @staticmethod
    async def test_claimed_rewards(client_instance: "DailyRewardClient"):
        claimed_rewards = await client_instance.claimed_rewards()
        assert claimed_rewards is not None

    @staticmethod
    @pytest.mark.xfail(raises=AlreadyClaimed, reason="Already claimed")
    async def test_claim_daily_reward(client_instance: "DailyRewardClient"):
        reward_result = await client_instance.claim_daily_reward()
        assert reward_result is not None
