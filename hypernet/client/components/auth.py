from hypernet.client.components.auth_client.oauth import AuthOAuthClient
from hypernet.client.components.auth_client.token import AuthTokenClient

__all__ = ("AuthClient",)


class AuthClient(
    AuthOAuthClient,
    AuthTokenClient,
):
    """
    The AuthClient class is a client for authentication services.
    """
