from typing import Optional, TYPE_CHECKING

__all__ = ("EndfieldBattleChronicleClient",)

from hypernet.client.base import BaseClient
from hypernet.errors import AccountNotFound
from hypernet.models.endfield.chronicle.notes import EndfieldNote, EndfieldNoteSkport
from hypernet.utils.enums import Region
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

    async def get_endfield_notes_by_info(
        self,
        cred: Optional[str] = None,
        player_id: Optional[int] = None,
        account_id: Optional[int] = None,
    ) -> EndfieldNoteSkport:
        """
        根据提供的信息获取 Endfield 笔记。

        该方法通过调用特定的 API 来获取 Endfield 笔记数据，并将返回的数据解析为 EndfieldNoteSkport 对象。

        Args:
            cred (Optional[str]): 用于请求的 cred cookie。如果未提供，则默认为 self.cookies.cred。
            player_id (Optional[int]): 用于请求的玩家 ID。如果未提供，则默认为实例的 player_id 属性。
            account_id (Optional[int]): 用于请求的账户 ID。如果未提供，则默认为实例的 account_id 属性。

        Returns:
            EndfieldNoteSkport: 包含笔记数据的 EndfieldNoteSkport 对象。

        Raises:
            AccountNotFound: 如果未找到有效的玩家 ID 或账户 ID。
        """
        self.region_specific(False)
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
        return EndfieldNoteSkport(**req["detail"], player_id=player_id)

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
        request_player_id: Optional[bool] = True,
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
            request_player_id (Optional[bool]): Whether to request the player ID. Defaults to True.

        Returns:
            EndfieldNote: The retrieved Endfield notes.

        Raises:
            AccountNotFound: If no default account or player ID is found.
        """
        if self.region is Region.CHINESE:
            return await self.get_endfield_notes_by_widget(cred=cred, request_player_id=request_player_id)
        else:
            data = await self.get_endfield_notes_by_info(cred=cred, player_id=player_id, account_id=account_id)
            return EndfieldNote.from_skport(data)
