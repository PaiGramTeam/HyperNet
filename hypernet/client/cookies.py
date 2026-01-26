from http.cookiejar import CookieJar
from http.cookies import SimpleCookie
from typing import Optional, TypeVar

from httpx import Cookies as _Cookies
from pydantic import BaseModel

from hypernet.utils.types import CookieTypes

IntStr = TypeVar("IntStr", int, str)

__all__ = (
    "Cookies",
    "CookiesModel",
)


class Cookies(_Cookies):
    """A wrapper around `httpx.Cookies` that provides additional functionality."""

    jar: CookieJar

    def __init__(self, cookies: Optional[CookieTypes] = None):  # skipcq: PYL-W0231
        self.jar = CookieJar()
        if cookies is None or isinstance(cookies, dict):
            if isinstance(cookies, dict):
                for key, value in cookies.items():
                    if isinstance(value, str):
                        self.set(key, value)
                    else:
                        self.set(key, str(value))
        elif isinstance(cookies, list):
            for key, value in cookies:
                self.set(key, value)
        elif isinstance(cookies, Cookies):
            for cookie in cookies.jar:
                self.jar.set_cookie(cookie)
        elif isinstance(cookies, str):
            cookie = SimpleCookie(cookies)
            for key, value in cookie.items():
                self.set(key, value.value)
        else:
            self.jar = cookies  # type: ignore

    @property
    def hg_token(self) -> Optional[str]:
        return self.get("hg_token")

    @hg_token.setter
    def hg_token(self, value: str) -> None:
        self.set("hg_token", value)

    @property
    def cred(self) -> Optional[str]:
        return self.get("cred")

    @cred.setter
    def cred(self, value: str) -> None:
        self.set("cred", value)

    @property
    def hg_id(self) -> Optional[IntStr]:
        hg_id = self.get("hg_id")
        if hg_id is not None:
            try:
                return int(hg_id)
            except ValueError:
                return hg_id
        return None

    @hg_id.setter
    def hg_id(self, value: IntStr) -> None:
        self.set("hg_id", str(value))

    @property
    def lab_user_id(self) -> Optional[IntStr]:
        lab_user_id = self.get("lab_user_id")
        if lab_user_id is not None:
            try:
                return int(lab_user_id)
            except ValueError:
                return lab_user_id
        return None

    @lab_user_id.setter
    def lab_user_id(self, value: IntStr) -> None:
        self.set("lab_user_id", str(value))

    def get(
        self,
        name: str,
        default: Optional[str] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
    ) -> Optional[str]:
        """
        Get a cookie by name. May optionally include domain and path
        in order to specify exactly which cookie to retrieve.
        """
        value = None
        for cookie in self.jar:
            if (
                cookie.name == name
                and domain is None
                or cookie.domain == domain
                and path is None
                or cookie.path == path
                and cookie.value
            ):
                value = cookie.value
        if value is None:
            return default
        return value


class CookiesModel(BaseModel, frozen=False):
    """A model that represents the cookies used by the client."""

    hg_token: Optional[str] = None
    hg_id: Optional[IntStr] = None

    cred: Optional[str] = None
    lab_user_id: Optional[IntStr] = None

    def to_dict(self):
        """Return the cookies as a dictionary."""
        return self.dict(exclude_defaults=True)

    def to_json(self):
        """Return the cookies as a JSON string."""
        return self.json(exclude_defaults=True)
