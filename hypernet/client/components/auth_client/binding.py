from typing import Optional

from hypernet.client.base import BaseClient
from hypernet.client.routes import BINDING_BASE_API_URL

from hypernet.models.lab.game_role import GameRole, GameRoleId

__all__ = ("AuthBindingClient",)


class AuthBindingClient(BaseClient):
    """
    AuthBindingClient 类是一个用于身份验证服务的客户端。
    它继承自 BaseClient 类，并提供了用于检索不同身份验证令牌和密钥的方法。
    """

    async def get_game_accounts_by_binding_token(
        self,
        binding_token: str,
    ) -> list[GameRole]:
        """
        根据绑定令牌获取游戏账户列表。

        :param binding_token: 绑定令牌，用于标识用户的绑定信息。
        :return: 包含 GameRole 对象的列表，表示用户的游戏账户信息。
        """
        path = "account/binding/v1/binding_list"
        url = BINDING_BASE_API_URL.get_url(self.region) / path
        params = {"token": binding_token}
        headers = self.get_default_header({}, False)
        req = await self.request_api("GET", url=url, params=params, headers=headers)
        return [GameRole(**item) for item in req.get("list", [])]

    async def get_role_id_by_player_id(
        self,
        binding_token: str,
        player_id: Optional[int] = None,
    ) -> Optional[GameRoleId]:
        """
        根据玩家 ID 和绑定令牌获取角色 ID。

        :param binding_token: 绑定令牌，用于标识用户的绑定信息。
        :param player_id: 玩家 ID，可选参数。如果未提供，则使用默认的 player_id。
        :return: 一个 GameRoleId 对象，包含角色 ID、频道 ID 和服务器 ID。如果未找到匹配的角色，返回 None。
        """
        player_id = player_id or self.player_id
        game_accounts = await self.get_game_accounts_by_binding_token(binding_token)
        for account in game_accounts:
            for bind in account.bindingList:
                for role in bind.roles:
                    if role.uid == int(player_id):
                        return GameRoleId(
                            player_id=player_id,
                            role_id=bind.uid,
                            channel_id=bind.channelMasterId,
                            server_id=role.serverId,
                        )
        return None

    async def get_role_token_by_binding_token(
        self,
        binding_token: str,
        role_id: str,
    ) -> str:
        """
        根据绑定令牌和角色 ID 获取角色令牌。

        :param binding_token: 绑定令牌，用于标识用户的绑定信息。
        :param role_id: 角色 ID，用于标识具体的角色。
        :return: 角色令牌字符串。
        """
        path = "account/binding/v1/u8_token_by_uid"
        url = BINDING_BASE_API_URL.get_url(self.region) / path
        headers = self.get_default_header({}, True)
        data = {
            "uid": role_id,
            "token": binding_token,
        }
        req = await self.request_api(
            "POST",
            url,
            json=data,
            headers=headers,
        )
        return req["token"]
