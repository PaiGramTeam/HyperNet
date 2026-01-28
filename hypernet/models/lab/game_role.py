from typing import List, Optional, Any

from pydantic import model_validator

from hypernet.models.base import APIModel, Field, DateTimeField


class GameRoleBindingRole(APIModel):
    """
    表示游戏角色绑定的角色信息。

    属性:
        isBanned (bool): 是否被封禁。
        serverId (str): 服务器 ID。
        serverName (str): 服务器名称。
        uid (int): 角色 ID，字段别名为 roleId。
        nickname (Optional[str]): 角色昵称，可选。
        level (int): 角色等级。
        isDefault (bool): 是否为默认角色。
        serverType (Optional[str]): 服务器类型，可选。
        registerTs (Optional[DateTimeField]): 注册时间戳，可选。
    """

    isBanned: bool
    serverId: str
    serverName: str

    uid: int = Field(alias="roleId")
    nickname: Optional[str] = None
    level: int

    isDefault: bool
    serverType: Optional[str] = None
    registerTs: Optional[DateTimeField] = None

    @model_validator(mode="before")
    @classmethod
    def unify_nickname_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        统一处理 nickname 字段，确保数据一致性。

        :param data: 包含角色信息的字典。
        :return: 处理后的字典。
        """
        if isinstance(data, dict):
            # 统一处理 nickname 字段
            nickname_value = data.get("nickname") or data.get("nickName")
            if nickname_value:
                data["nickname"] = nickname_value
                if "nickName" in data:
                    del data["nickName"]  # 移除多余的字段
        return data


class GameRoleBindingListItem(APIModel):
    """
    表示游戏角色绑定列表中的一项。

    属性:
        uid (str): 用户 ID。
        isOfficial (bool): 是否为官方绑定。
        isDefault (bool): 是否为默认绑定。
        channelMasterId (str): 渠道主 ID。
        channelName (str): 渠道名称。
        nickName (Optional[str]): 昵称，可选。
        isDelete (Optional[bool]): 是否已删除，可选。
        isBanned (Optional[bool]): 是否被封禁，可选。
        gameName (Optional[str]): 游戏名称，可选。
        gameId (Optional[str]): 游戏 ID，可选。
        roles (List[GameRoleBindingRole]): 绑定的角色列表。
        defaultRole (Optional[GameRoleBindingRole]): 默认角色，可选。
    """

    uid: str
    isOfficial: bool
    isDefault: bool
    channelMasterId: str
    channelName: str
    nickName: Optional[str] = None
    isDelete: Optional[bool] = None
    isBanned: Optional[bool] = None
    gameName: Optional[str] = None
    gameId: Optional[str] = None
    roles: List[GameRoleBindingRole]
    defaultRole: Optional[GameRoleBindingRole] = None


class GameRole(APIModel):
    """
    表示游戏角色信息。

    属性:
        appCode (str): 应用代码。
        appName (str): 应用名称。
        bindingList (List[GameRoleBindingListItem]): 绑定列表。
    """

    appCode: str
    appName: str
    bindingList: List[GameRoleBindingListItem]


class GameRoleId(APIModel):
    """
    表示游戏角色的唯一标识。

    属性:
        player_id (int): 玩家 ID。
        role_id (str): 角色 ID。
        channel_id (str): 渠道 ID。
        server_id (str): 服务器 ID。
    """

    player_id: int
    role_id: str
    channel_id: str
    server_id: str
