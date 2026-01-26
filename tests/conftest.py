import asyncio
import os
import warnings
from pathlib import Path
from typing import Optional

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from hypernet.client.components.auth import AuthClient
from hypernet.client.cookies import Cookies
from hypernet.utils.cookies import parse_cookie
from hypernet.utils.enums import Region

env_path = Path(".env")
if env_path.exists():
    load_dotenv()


@pytest.fixture(scope="session")
def event_loop():  # skipcq: PY-D0003
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        loop = asyncio.get_event_loop()

    yield loop
    loop.close()


@pytest.fixture(scope="session")
def region() -> Region:  # skipcq: PY-D0003
    _region = os.environ.get("REGION")
    if not _region:
        return Region.CHINESE
    return Region(_region)


__cookies = None


@pytest_asyncio.fixture(loop_scope="session")
async def cookies(region: Region) -> "Cookies":  # skipcq: PY-D0003
    global __cookies
    if __cookies:
        return __cookies
    cookies_str = os.environ.get("COOKIES")
    if not cookies_str:
        pytest.exit("No cookies set", 1)

    _cookies = Cookies(parse_cookie(cookies_str))
    if _cookies.hg_id is None:
        warnings.warn(UserWarning("can not found hg id in cookies"), stacklevel=2)

    if not _cookies.cred:
        async with AuthClient(cookies=_cookies, region=region) as auth_client:
            _cookies = await auth_client.refresh_cookies_by_hg_token()
    __cookies = _cookies

    return _cookies


@pytest.fixture(scope="session")
def endfield_player_id() -> Optional[int]:  # skipcq: PY-D0003
    _player_id = os.environ.get("ENDFIELD_PLAYER_ID")
    if not _player_id:
        warnings.warn(UserWarning("No endfield player id set"), stacklevel=2)
        return None
    return int(_player_id)
