import logging
import typing
from contextlib import AbstractAsyncContextManager
from json import JSONDecodeError
from types import TracebackType

from httpx import AsyncClient, HTTPError, Response, Timeout, TimeoutException

from hypernet.client.cookies import Cookies
from hypernet.client.headers import Headers
from hypernet.client.routes import BASE_API_URL
from hypernet.errors import (
    BadRequest,
    NetworkError,
    NotSupported,
    RegionNotSupported,
    TimedOut,
    raise_for_ret_code,
)
from hypernet.utils.device_fp import SklandDeviceFP
from hypernet.utils.ds import generate_dynamic_secret, SklandSign
from hypernet.utils.enums import Game, Region
from hypernet.utils.types import (
    RT,
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestData,
    TimeoutTypes,
    URLTypes,
)

_LOGGER = logging.getLogger("HyperNet.BaseClient")

__all__ = ("BaseClient",)


class BaseClient(AbstractAsyncContextManager["BaseClient"]):
    """
    This is the base class for hypernet clients. It provides common methods and properties for hypernet clients.

    Args:
        cookies (typing.Optional[str, CookieTypes], typing.Optional): The cookies used for the client.
        headers (typing.Optional[HeaderTypes], typing.Optional): The headers used for the client.
        hg_id (typing.Optional[int], typing.Optional): The account id used for the client.
        player_id (typing.Optional[int], typing.Optional): The player id used for the client.
        region (Region, typing.Optional): The region used for the client.
        lang (str, typing.Optional): The language used for the client.
        timeout (typing.Optional[TimeoutTypes], typing.Optional): Timeout configuration for the client.

    Attributes:
        headers (HeaderTypes): The headers used for the client.
        hg_id (typing.Optional[int]): The account id used for the client.
        player_id (typing.Optional[int]): The player id used for the client.
        region (Region): The region used for the client.
        lang (str): The language used for the client.
        game (typing.Optional[Game]): The game used for the client.

    """

    game: typing.Optional[Game] = None

    def __init__(
        self,
        cookies: typing.Optional[typing.Union[str, CookieTypes]] = None,
        headers: typing.Optional[HeaderTypes] = None,
        hg_id: typing.Optional[int] = None,
        account_id: typing.Optional[int] = None,
        player_id: typing.Optional[int] = None,
        region: Region = Region.OVERSEAS,
        lang: str = "zh-cn",
        timeout: typing.Optional[TimeoutTypes] = None,
    ) -> None:
        """Initialize the client with the given parameters."""
        if timeout is None:
            timeout = Timeout(
                connect=5.0,
                read=5.0,
                write=5.0,
                pool=1.0,
            )
        self._cookies = Cookies(cookies)
        self.headers = Headers(headers)
        self.player_id = player_id
        self.hg_id = hg_id or self._cookies.hg_id
        self.account_id = account_id or self._cookies.lab_user_id
        self.client = AsyncClient(timeout=timeout)
        self.region = region
        self.lang = lang
        self.lang2 = {"zh-cn": "zh_Hans"}.get(lang, "zh_Hans")

    @property
    def cookies(self) -> Cookies:
        """Get the cookies used for the client."""
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: CookieTypes) -> None:
        self._cookies = Cookies(cookies)

    @staticmethod
    async def get_device_id() -> str:
        return await SklandDeviceFP().get_cached_device_id()

    @staticmethod
    async def get_sign_token() -> str:
        return await SklandSign().get_cached_sign_token()

    @property
    def app_version(self) -> str:
        """Get the app version used for the client."""
        if self.region == Region.CHINESE:
            return "1.0.0"
        if self.region == Region.OVERSEAS:
            return "1.5.0"
        return "null"

    @property
    def client_type(self) -> str:
        """Get the client type used for the client."""
        if self.region == Region.CHINESE:
            return "3"
        if self.region == Region.OVERSEAS:
            return "5"
        return "null"

    @property
    def user_agent(self) -> str:
        """Get the user agent used for the client."""
        if self.region == Region.CHINESE:
            return "Skland/1.28.0 (com.hypergryph.skland; build:102800063; Android 35; ) Okhttp/4.11.0"
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.116 Safari/537.36"
        )

    async def __aenter__(self: RT) -> RT:
        """Enter the async context manager and initialize the client."""
        try:
            await self.initialize()
        except Exception:
            await self.shutdown()
            raise
        return self

    async def __aexit__(
        self,
        exc_type: typing.Optional[type[BaseException]],
        exc_val: typing.Optional[BaseException],
        exc_tb: typing.Optional[TracebackType],
    ) -> None:
        """Exit the async context manager and shutdown the client."""
        await self.shutdown()

    async def shutdown(self):
        """Shutdown the client."""
        if self.client.is_closed:
            _LOGGER.info("This Client is already shut down. Returning.")
            return

        await self.client.aclose()

    async def initialize(self):
        """Initialize the client."""

    def get_default_header(self, headers: HeaderTypes, is_json: bool):
        """Get the default header for API requests.

        Args:
            headers (HeaderTypes): The header to use.
            is_json (bool): Whether the request is JSON.

        Returns:
            Headers: The default header with added fields.
        """
        headers = Headers(headers)
        headers["Connection"] = "close"
        if is_json:
            headers["Content-Type"] = "application/json"
        headers["user-agent"] = self.user_agent
        headers["x-language"] = self.lang
        headers["sk-language"] = self.lang2
        return headers

    async def request(
        self,
        method: str,
        url: URLTypes,
        data: typing.Optional[RequestData] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
    ) -> Response:
        """Make an HTTP request and return the response.

        This method makes an HTTP request with the specified HTTP method, URL, request parameters, headers,
        and JSON payload. It catches common HTTP errors and raises a `NetworkError` or `TimedOut` exception
        if the request times out.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            data (typing.Optional[RequestData]): The request data to include in the body of the request.
            json (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Response: A `Response` object representing the HTTP response.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.

        """
        try:
            return await self.client.request(
                method,
                url,
                data=data,
                json=json,
                params=params,
                headers=headers,
            )
        except TimeoutException as exc:
            raise TimedOut from exc
        except HTTPError as exc:
            raise NetworkError from exc

    async def request_api(
        self,
        method: str,
        url: URLTypes,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
    ):
        """Make an API request and return the data.

        This method makes an API request using the `request()` method
        and returns the data from the response if it is successful.
        If the response contains an error, it raises a `BadRequest` exception.

        Args:
            method (str): The HTTP method to use for the request (e.g., "GET", "POST").
            url (URLTypes): The URL to send the request to.
            json (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.

        Returns:
            Any: The data returned by the API.

        Raises:
            NetworkError: If an HTTP error occurs while making the request.
            TimedOut: If the request times out.
            BadRequest: If the response contains an error.
        """
        response = await self.request(
            method,
            url,
            json=json,
            params=params,
            headers=headers,
        )
        if not response.is_error:
            data = response.json()
            ret_code = data.get("code", 0)
            if ret_code != 0:
                raise_for_ret_code(data)
            return data["data"]
        if response.status_code == 404:
            raise NotSupported("API not supported or has been removed.")
        try:
            data = response.json()
            ret_code = data.get("code", 0)
            if ret_code != 0:
                raise_for_ret_code(data)
        except JSONDecodeError:
            pass
        raise BadRequest(status_code=response.status_code, message=response.text)

    async def request_lab(
        self,
        url: URLTypes,
        method: typing.Optional[str] = None,
        data: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cred: typing.Optional[str] = None,
    ):
        """Make a request to the lab API and return the data.

        This method makes a request to the lab API using the `request_api()` method
        and returns the data from the response if it is successful.
        It also adds headers for the lab API and handles the case where the method is not specified.

        Args:
            url (URLTypes): The URL to send the request to.
            method (typing.Optional[str]): The HTTP method to use for the request (e.g., "GET", "POST").
            data (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.
            cred (typing.Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            Any: The data returned by the lab API.

        """
        if method is None:
            method = "POST" if data else "GET"

        headers = self.get_default_header(headers, method == "POST")
        cred = cred or self.cookies.cred
        token = await self.get_sign_token()
        if cred is not None:
            headers["cred"] = cred
        if token is not None:
            sign, header_ca = generate_dynamic_secret(token, url, method, params, data)
            headers.update(header_ca)
            headers["sign"] = sign

        return await self.request_api(method=method, url=url, json=data, params=params, headers=headers)

    async def request_base_api(
        self,
        path: str,
        method: typing.Optional[str] = None,
        data: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cred: typing.Optional[str] = None,
    ):
        """Make a request to the base API and return the data.

        This method constructs the full API URL from the given path and makes a request
        to the lab API using the `request_lab()` method.

        Args:
            path (str): The API path to request.
            method (typing.Optional[str]): The HTTP method to use for the request (e.g., "GET", "POST").
            data (typing.Optional[Any]): The JSON payload to include in the body of the request.
            params (typing.Optional[QueryParamTypes]): The query parameters to include in the request.
            headers (typing.Optional[HeaderTypes]): The headers to include in the request.
            cred (typing.Optional[str]): The cred cookie to use for the request. Defaults to self.cookies.cred if not provided.

        Returns:
            Any: The data returned by the API.

        """
        url = BASE_API_URL.get_url(self.region) / path
        return await self.request_lab(
            url=url,
            method=method,
            data=data,
            params=params,
            headers=headers,
            cred=cred,
        )

    def region_specific(self, cn: bool) -> None:
        """Prevent function to be run with unsupported regions."""
        if cn and self.region != Region.CHINESE:
            raise RegionNotSupported
        if not cn and self.region == Region.CHINESE:
            raise RegionNotSupported
