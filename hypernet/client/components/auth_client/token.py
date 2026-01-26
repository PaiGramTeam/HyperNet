from hypernet.client.base import BaseClient

__all__ = ("AuthTokenClient",)


class AuthTokenClient(BaseClient):
    """
    The AuthTokenClient class is a client for authentication services.
    It is derived from the BaseClient class and provides methods for retrieving
    different authentication tokens and keys.
    """

    async def refresh_sign_token(self) -> str:
        path = "auth/refresh"
        cred = "abc123"
        headers = {
            "sign_enable": "false",
        }
        req = await self.request_base_api(path, headers=headers, cred=cred)
        return req["token"]
