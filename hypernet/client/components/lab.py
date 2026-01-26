from typing import Optional

from hypernet.client.base import BaseClient
from hypernet.models.lab.account import UserCheckInfo
from hypernet.models.lab.game_role import GameRole
from hypernet.utils.enums import Game

__all__ = ("LabClient",)


class LabClient(BaseClient):
    """LabClient component."""

    async def check_lab_user(
        self,
        cred: Optional[str] = None,
    ) -> UserCheckInfo:
        """Check if the user is a lab user.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.):
        Returns:
            UserCheckInfo: The user check info object.
        """
        path = "user/check"
        req = await self.request_base_api(path, cred=cred)
        return UserCheckInfo(**req)

    async def get_game_accounts(
        self,
        cred: Optional[str] = None,
    ) -> list[GameRole]:
        """Get the game accounts of the currently logged-in user.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            List[GameRole]: A list of game role objects.
        """
        path = "game/player/binding"
        req = await self.request_base_api(path, cred=cred)
        return [GameRole(**item) for item in req.get("list", [])]

    async def get_arknights_accounts(
        self,
        cred: Optional[str] = None,
    ) -> list[GameRole]:
        """Get the Arknights game accounts of the currently logged-in user.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            List[GameRole]: A list of Arknights game role objects.
        """
        accounts = await self.get_game_accounts(cred=cred)
        return [account for account in accounts if account.appCode == Game.ARKNIGHTS.value]

    async def get_endfield_accounts(
        self,
        cred: Optional[str] = None,
    ) -> list[GameRole]:
        """Get the Endfield game accounts of the currently logged-in user.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            List[GameRole]: A list of Endfield game role objects.
        """
        accounts = await self.get_game_accounts(cred=cred)
        return [account for account in accounts if account.appCode == Game.ENDFIELD.value]
