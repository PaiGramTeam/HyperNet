from typing import Optional, TYPE_CHECKING

__all__ = ("EndfieldBattleChronicleClient",)

from hypernet.client.base import BaseClient
from hypernet.errors import AccountNotFound
from hypernet.models.endfield.chronicle.card import EndfieldCardDetail
from hypernet.models.endfield.chronicle.notes import EndfieldNote
from hypernet.utils.player import recognize_endfield_server

if TYPE_CHECKING:
    from hypernet.models.lab.game_role import GameRole


class EndfieldBattleChronicleClient(BaseClient):
    """A client for retrieving data from Endfield's battle chronicle component.

    This class is used to retrieve various data objects from StarRail's battle chronicle component,
    including real-time notes, user statistics, and character information.
    """

    async def get_default_endfield_account_id(
        self,
        cred: Optional[str] = None,
    ) -> int:
        """Get the default Endfield account ID.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            int: The default Endfield account ID.

        Raises:
            AccountNotFound: If no default account is found.
        """
        players: list["GameRole"] = await self.get_endfield_accounts(cred=cred)
        if not players:
            raise AccountNotFound()
        for player in players:
            for bind in player.bindingList:
                if role := bind.defaultRole:
                    return role.uid
        raise AccountNotFound()

    async def get_endfield_card_detail(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ) -> EndfieldCardDetail:
        """
        Retrieve detailed information about an Endfield card.

        This method fetches the details of an Endfield card for a specific player and account.
        It constructs the necessary API request and processes the response to return the card details.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.
            player_id (Optional[int]): The player ID to use for the request. Defaults to self.player_id if not provided.
            account_id (Optional[int]): The account ID to use for the request. Defaults to self.account_id if not provided.

        Returns:
            EndfieldCardDetail: The detailed information about the Endfield card.

        Raises:
            AccountNotFound: If the player ID or account ID is not provided or cannot be determined.
        """
        player_id = player_id or self.player_id
        account_id = account_id or self.account_id
        if not player_id or not account_id:
            raise AccountNotFound()
        server_id = recognize_endfield_server(player_id)
        path = "game/endfield/card/detail"
        params = {
            "roleId": player_id,
            "serverId": server_id,
            "userId": account_id,
        }
        req = await self.request_base_api(path, params=params, cred=cred)
        return EndfieldCardDetail(**req["detail"], player_id=player_id)

    async def get_endfield_notes_by_widget(
        self,
        cred: Optional[str] = None,
        request_player_id: Optional[bool] = True,
    ) -> EndfieldNote:
        """Get Endfield's real-time notes.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.
            request_player_id (Optional[bool]): Whether to request the player ID. Defaults to True.

        Returns:
            EndfieldNote: The requested real-time notes.

        Raises:
            AccountNotFound: If no default account is found.
        """
        self.region_specific(True)
        player_id = 0
        if request_player_id:
            player_id = await self.get_default_endfield_account_id(cred=cred)
        path = "game/endfield/statistic"
        req = await self.request_base_api(path, cred=cred)
        return EndfieldNote(**req["data"], player_id=player_id)

    async def get_endfield_notes(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ) -> EndfieldNote:
        """
        Retrieve Endfield notes based on the region.

        Depending on the region, this method fetches Endfield notes either via the widget API
        or the info API. The method determines the appropriate API to use and processes the
        response accordingly.

        Args:
            cred (Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.
            player_id (Optional[int]): The player ID to use for the request. Defaults to None.
            account_id (Optional[int]): The account ID to use for the request. Defaults to None.

        Returns:
            EndfieldNote: The retrieved Endfield notes.

        Raises:
            AccountNotFound: If no default account or player ID is found.
        """
        data = await self.get_endfield_card_detail(cred=cred, player_id=player_id, account_id=account_id)
        return EndfieldNote.from_skport(data)
