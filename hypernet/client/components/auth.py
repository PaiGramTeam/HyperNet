from hypernet.client.components.auth_client.binding import AuthBindingClient
from hypernet.client.components.auth_client.oauth import AuthOAuthClient
from hypernet.client.components.auth_client.token import AuthTokenClient
from hypernet.client.components.auth_client.role import AuthRoleTokenClient

__all__ = ("AuthClient",)


class AuthClient(
    AuthBindingClient,
    AuthOAuthClient,
    AuthRoleTokenClient,
    AuthTokenClient,
):
    """
    The AuthClient class is a client for authentication services.
    """
