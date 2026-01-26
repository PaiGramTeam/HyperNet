from typing import List, Optional

from hypernet.models.base import APIModel


class GameRoleBindingRole(APIModel):
    serverId: int
    roleId: int
    nickname: str
    level: int
    isDefault: bool
    isBanned: bool
    serverType: str
    serverName: str


class GameRoleBindingListItem(APIModel):
    uid: int
    isOfficial: bool
    isDefault: bool
    channelMasterId: int
    channelName: str
    nickName: str
    isDelete: bool
    gameName: str
    gameId: int
    roles: List[GameRoleBindingRole]
    defaultRole: Optional[GameRoleBindingRole]


class GameRole(APIModel):
    appCode: str
    appName: str
    bindingList: List[GameRoleBindingListItem]
