from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from hypernet.client.components.chronicle.endfield import EndfieldBattleChronicleClient

if TYPE_CHECKING:
    from hypernet.client.cookies import Cookies
    from hypernet.utils.enums import Region


@pytest_asyncio.fixture
async def endfield_client(endfield_player_id: int, region: "Region", cookies: "Cookies"):
    if endfield_player_id is None:
        pytest.skip("Test case test_endfield_battle_chronicle_client skipped: No endfield player id set.")
    async with EndfieldBattleChronicleClient(
        player_id=endfield_player_id,
        cookies=cookies,
        region=region,
    ) as client_instance:
        yield client_instance


@pytest.mark.asyncio
class TestEndfieldBattleChronicleClient:
    @staticmethod
    async def test_get_endfield_notes(endfield_client: "EndfieldBattleChronicleClient"):
        notes = await endfield_client.get_endfield_notes(request_player_id=False)
        assert notes is not None
