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
    The AuthOAuthClient class is a client for authentication services.
    It is derived from the BaseClient class and provides methods for retrieving
    different authentication tokens and keys.
    """

    async def get_grant_code_by_hg_token(
        self,
        app: Optional[AppCode] = None,
        hg_token: Optional[str] = None,
        code_type: Optional[int] = 0,
    ) -> dict:
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
