from hypernet.client.base import BaseClient

__all__ = ("AuthRoleTokenClient",)

from hypernet.client.routes import GAME_HUB_BASE_API_URL


class AuthRoleTokenClient(BaseClient):
    """
    AuthRoleTokenClient 类是一个用于身份验证服务的客户端。
    它继承自 BaseClient 类，并提供了用于检索不同身份验证令牌和密钥的方法。
    """

    async def redeem_gift_code_by_role_token(
        self,
        code: str,
        role_token: str,
        server_id: str = "1",
        platform: str = "Windows",
        channel_id: str = "1",
    ) -> dict:
        """
        使用角色令牌兑换礼品码。

        :param code: 礼品码字符串。
        :param role_token: 角色令牌，用于标识用户的角色。
        :param server_id: 服务器 ID，默认为 "1"。
        :param platform: 平台名称，默认为 "Windows"。
        :param channel_id: 渠道 ID，默认为 "1"。
        :return: 包含兑换结果的字典。
        """
        path = "giftcode/api/redeem"
        url = GAME_HUB_BASE_API_URL.get_url(self.region) / path
        headers = self.get_default_header({}, True)
        data = {
            "code": code,
            "token": role_token,
            "serverId": str(server_id),
            "platform": platform,
            "channelId": str(channel_id),
            "confirm": False,
        }
        req = await self.request_api(
            "POST",
            url,
            json=data,
            headers=headers,
        )
        return req
