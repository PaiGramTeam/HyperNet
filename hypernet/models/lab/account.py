from typing import Optional

from hypernet.models.base import APIModel


class AccountInfo(APIModel):
    hgId: int
    email: Optional[str] = None
    phone: Optional[str] = None


class UserCheckInfo(APIModel):
    isNewUser: Optional[bool] = True
    nickname: Optional[str] = None
