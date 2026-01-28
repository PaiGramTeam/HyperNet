import base64
from typing import Union
from urllib.parse import urljoin

from httpx import URL as _URL

from hypernet.errors import NotSupported, RegionNotSupported
from hypernet.utils.enums import Game, Region

URLTypes = Union["URL", str]

__all__ = (
    "URL",
    "BaseRoute",
    "Route",
    "InternationalRoute",
    "GameRoute",
    "BASE_API_URL",
    "AS_BASE_API_URL",
    "BINDING_BASE_API_URL",
    "U8_BASE_API_URL",
    "GAME_HUB_BASE_API_URL",
)


class URL(_URL):
    """A subclass of httpx's URL class, with additional convenience methods for URL manipulation."""

    def join(self, url: URLTypes) -> "URL":
        """
        Join the current URL with the given URL.

        Args:
            url (Union[URL, str]): The URL to join with.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self), str(URL(url))))

    def __truediv__(self, url: URLTypes) -> "URL":
        """
        Append the given URL to the current URL using the '/' operator.

        Args:
            url (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return URL(urljoin(str(self) + "/", str(URL(url))))

    def __bool__(self):
        """Return True if the URL is not empty.

        Returns:
            bool: True if the URL is not empty.

        """
        return str(self) != ""

    def replace(self, old: str, new: str) -> "URL":
        """
        Replace a substring in the URL.

        Args:
            old (str): The substring to replace.
            new (str): The new substring to replace with.

        Returns:
            URL: A new URL instance with the substring replaced.

        """
        return URL(str(self).replace(old, new))


class BaseRoute:
    """A base class for defining routes with useful metadata."""


class Route(BaseRoute):
    """A standard route with a single URL."""

    url: URL

    def __init__(self, url: str) -> None:
        """
        Initialize a Route instance.

        Args:
            url (str): The URL for this route.

        """
        self.url = URL(url)

    def get_url(self) -> URL:
        """
        Get the URL for this route.

        Returns:
            URL: The URL for this route.

        """
        return self.url

    def __truediv__(self, other: str) -> URL:
        """
        Append the given URL to this route using the '/' operator.

        Args:
            other (Union[URL, str]): The URL to append.

        Returns:
            URL: A new URL instance representing the joined URL.

        """
        return self.url / other


class InternationalRoute(BaseRoute):
    """A route with URLs for both the overseas and Chinese regions."""

    urls: dict[Region, URL]

    def __init__(self, overseas: str, chinese: str) -> None:
        """
        Initialize an InternationalRoute instance.

        Args:
            overseas (str): The URL for the overseas region.
            chinese (str): The URL for the Chinese region.

        """
        self.urls = {
            Region.OVERSEAS: URL(overseas),
            Region.CHINESE: URL(chinese),
        }

    def get_url(self, region: Region) -> URL:
        """
        Get the URL for the given region.

        Args:
            region (Region): The region to get the URL for.

        Returns:
            URL: The URL for the given region.

        Raises:
            RegionNotSupported: If the given region is not supported.

        """
        if not self.urls[region]:
            raise RegionNotSupported(f"URL does not support {region.name} region.")

        return self.urls[region]


class GameRoute(BaseRoute):
    """A route with URLs for different games and regions."""

    urls: dict[Region, dict[Game, URL]]

    def __init__(
        self,
        overseas: dict[str, str],
        chinese: dict[str, str],
    ) -> None:
        """
        Initialize a GameRoute instance.

        Args:
            overseas (Dict[str, str]): A dictionary mapping game names to URLs for the overseas region.
            chinese (Dict[str, str]): A dictionary mapping game names to URLs for the Chinese region.

        """
        self.urls = {
            Region.OVERSEAS: {Game(game): URL(url) for game, url in overseas.items()},
            Region.CHINESE: {Game(game): URL(url) for game, url in chinese.items()},
        }

    def get_url(self, region: Region, game: Game) -> URL:
        """
        Get the URL for the given region and game.

        Args:
            region (Region): The region to get the URL for.
            game (Game): The game to get the URL for.

        Returns:
            URL: The URL for the given region and game.

        Raises:
            RegionNotSupported: If the given region is not supported.
            GameNotSupported: If the given game is not supported.

        """
        if not self.urls[region]:
            raise RegionNotSupported(f"URL does not support {region.name} region.")

        if not self.urls[region][game]:
            raise NotSupported(f"URL does not support {game.name} game for {region.name} region.")

        return self.urls[region][game]


BASE_API_URL = InternationalRoute(
    overseas="https://zonai.skport.com/api/v1",
    chinese="https://zonai.skland.com/api/v1",
)
AS_BASE_API_URL = InternationalRoute(
    overseas="https://as.gryphline.com",
    chinese="https://as.hypergryph.com",
)
BINDING_BASE_API_URL = InternationalRoute(
    overseas="https://binding-api-account-prod.gryphline.com",
    chinese="https://binding-api-account-prod.hypergryph.com",
)
U8_BASE_API_URL = InternationalRoute(
    overseas=base64.b64decode("aHR0cHM6Ly91OC5ncnlwaGxpbmUuY29t").decode(),
    chinese=base64.b64decode("aHR0cHM6Ly91OC5oeXBlcmdyeXBoLmNvbQ==").decode(),
)
GAME_HUB_BASE_API_URL = InternationalRoute(
    overseas="https://game-hub.gryphline.com",
    chinese="https://game-hub.hypergryph.com",
)
