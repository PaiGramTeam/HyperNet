from typing import Optional

from hypernet.client.components.auth import AuthClient
from hypernet.client.components.daily import DailyRewardClient
from hypernet.client.components.lab import LabClient
from hypernet.utils.enums import Game

__all__ = ("EndfieldClient",)


class EndfieldClient(
    AuthClient,
    DailyRewardClient,
    LabClient,
):
    """A simple http client for Endfield endpoints."""

    game: Optional[Game] = Game.ENDFIELD
