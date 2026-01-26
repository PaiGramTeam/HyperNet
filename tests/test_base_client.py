import pytest

from hypernet.client.base import BaseClient
from hypernet.client.cookies import Cookies


@pytest.mark.asyncio
class TestBaseClient:
    @staticmethod
    async def test_cookies():
        async with BaseClient(cookies={"uid": "114514"}) as client:
            assert isinstance(client.cookies, Cookies)
            client.cookies = {"hg_id": "114514"}
            assert isinstance(client.cookies, Cookies)
            assert client.cookies.hg_id == 114514
