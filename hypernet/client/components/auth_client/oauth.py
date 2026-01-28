from typing import Optional

from hypernet.client.base import BaseClient

__all__ = ("AuthOAuthClient",)

from hypernet.client.cookies import CookiesModel
from hypernet.client.routes import AS_BASE_API_URL, BASE_API_URL
from hypernet.errors import BadRequest
from hypernet.models.lab.account import AccountInfo
from hypernet.utils.ds import generate_signature
from hypernet.utils.enums import AppCode, Region


class AuthOAuthClient(BaseClient):
    """
    AuthOAuthClient 类是一个用于身份验证服务的客户端。
    它继承自 BaseClient 类，并提供了用于检索不同身份验证令牌和密钥的方法。
    """

    async def get_grant_code_by_hg_token(
        self,
        app: Optional[AppCode] = None,
        hg_token: Optional[str] = None,
        code_type: Optional[int] = 0,
    ) -> dict:
        """
        根据 hg_token 获取授权码。

        :param app: 应用代码，可选参数。如果未提供，将根据区域选择默认值。
        :param hg_token: 用户的 hg_token，可选参数。如果未提供，将使用默认的 cookies.hg_token。
        :param code_type: 授权码类型，可选参数，默认为 0。
        :return: 包含授权码的字典。
        """
        if not app:
            if self.region is Region.CHINESE:
                app = AppCode.SKLAND
            else:
                app = AppCode.SKPORT
        hg_token = hg_token or self.cookies.hg_token
        url = AS_BASE_API_URL.get_url(self.region) / "user/oauth2/v2/grant"
        headers = self.get_default_header({}, True)
        data = {
            "appCode": app.value,
            "type": int(code_type),
            "token": hg_token,
        }
        return await self.request_api(
            "POST",
            url,
            json=data,
            headers=headers,
        )

    async def get_account_info_by_hg_token(self, hg_token: Optional[str] = None) -> AccountInfo:
        """
        根据 hg_token 获取账户信息。

        :param hg_token: 用户的 hg_token，可选参数。如果未提供，将使用默认的 cookies.hg_token。
        :return: AccountInfo 对象，包含账户的基本信息。
        """
        hg_token = hg_token or self.cookies.hg_token
        url = AS_BASE_API_URL.get_url(self.region) / "user/info/v1/basic"
        headers = self.get_default_header({}, False)
        params = {
            "token": hg_token,
        }
        req = await self.request_api(
            "GET",
            url,
            params=params,
            headers=headers,
        )
        return AccountInfo(**req)

    async def check_hg_token(self, hg_token: Optional[str] = None) -> bool:
        """
        检查 hg_token 是否有效。

        :param hg_token: 用户的 hg_token，可选参数。如果未提供，将使用默认的 cookies.hg_token。
        :return: 如果有效返回 True，否则返回 False。
        """
        try:
            await self.get_account_info_by_hg_token(hg_token)
        except BadRequest as exc:
            if exc.status_code == 401:
                return False
            raise exc
        return True

    async def get_cred_by_grant_code(
        self,
        grant_code: str,
        kind: Optional[int] = 1,
    ) -> CookiesModel:
        """
        根据授权码获取凭证。

        :param grant_code: 授权码，用于生成凭证。
        :param kind: 凭证类型，可选参数，默认为 1。
        :return: CookiesModel 对象，包含生成的凭证信息。
        """
        url = BASE_API_URL.get_url(self.region) / "user/auth/generate_cred_by_code"
        device_id = await self.get_device_id()
        headers_pre = {
            "referer": "https://www.skland.com/" if self.region == Region.CHINESE else "https://www.skport.com/",
            "origin": "https://www.skland.com" if self.region == Region.CHINESE else "https://www.skport.com",
        }
        _, sign_headers = generate_signature("", "", "")
        headers_pre.update(sign_headers)
        headers_pre["dId"] = device_id
        headers = self.get_default_header(headers_pre, True)
        data = {
            "code": grant_code,
            "kind": int(kind),
        }
        req = await self.request_api(
            "POST",
            url,
            json=data,
            headers=headers,
        )
        cookie = CookiesModel()
        cookie.cred = req["cred"]
        cookie.lab_user_id = req["userId"]
        return cookie

    async def refresh_cookies_by_hg_token(
        self,
        hg_token: Optional[str] = None,
    ) -> CookiesModel:
        """
        根据 hg_token 刷新 cookies。

        :param hg_token: 用户的 hg_token，可选参数。如果未提供，将使用默认的 cookies.hg_token。
        :return: CookiesModel 对象，包含刷新后的 cookies 信息。
        """
        hg_token = hg_token or self.cookies.hg_token
        resp = await self.get_grant_code_by_hg_token(hg_token=hg_token)
        grant_code = resp["code"]
        cookies = await self.get_cred_by_grant_code(grant_code)
        cookies.hg_token = hg_token
        cookies.hg_id = self.cookies.hg_id
        cookies.lab_show_user_id = self.cookies.lab_show_user_id

        self.cookies.cred = cookies.cred
        self.cookies.lab_user_id = cookies.lab_user_id
        if self.region == Region.OVERSEAS:
            cookies.lab_show_user_id = cookies.lab_user_id
            self.cookies.lab_show_user_id = cookies.lab_user_id
        return cookies

    async def get_binding_token_by_hg_token(
        self,
        hg_token: Optional[str] = None,
    ) -> str:
        """
        根据 hg_token 获取绑定令牌。

        :param hg_token: 用户的 hg_token，可选参数。如果未提供，将使用默认的 cookies.hg_token。
        :return: 绑定令牌字符串。
        """
        app = AppCode.BINDING_CN if self.region is Region.CHINESE else AppCode.BINDING_OS
        oauth_token = await self.get_grant_code_by_hg_token(app=app, hg_token=hg_token, code_type=1)
        return oauth_token["token"]
