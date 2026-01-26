import asyncio
import hashlib
import hmac
import json
import time
import typing
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode

import httpx

from hypernet.utils.types import QueryParamTypes

header_for_sign = {
    "platform": "3",
    "timestamp": "",
    "dId": "",
    "vName": "1.0.0",
}


def generate_signature(token: str, path: str, body_or_query: str, did: str = "") -> tuple[str, dict[str, str]]:
    t = str(int(time.time()) - 1)
    _token = token.encode("utf-8")
    header_ca = header_for_sign.copy()
    header_ca["timestamp"] = t
    header_ca["dId"] = did
    header_ca_str = json.dumps(header_ca, separators=(",", ":"))
    s = path + body_or_query + t + header_ca_str
    hex_s = hmac.new(_token, s.encode("utf-8"), hashlib.sha256).hexdigest()
    md5 = hashlib.md5(hex_s.encode("utf-8")).hexdigest()
    return md5, header_ca


def generate_dynamic_secret(
    token: str,
    url: str,
    method: str = "get",
    data: typing.Any = None,
    params: typing.Optional[QueryParamTypes] = None,
):
    p = urlparse(str(url))
    if method.lower() == "get":
        if params:
            if isinstance(params, str):
                # If params is a JSON string, parse it to dict first
                params_dict = json.loads(params)
                query_str = urlencode(params_dict)
            else:
                # If params is a dict, encode it directly
                query_str = urlencode(params)
        else:
            query_str = ""
        sign, header_ca = generate_signature(token, p.path, query_str)
    else:
        sign, header_ca = generate_signature(token, p.path, json.dumps(data) if data is not None else "")
    return sign, header_ca


class SklandSign:
    # 单例模式实现
    _instance = None
    _lock = asyncio.Lock()

    # 缓存相关
    _cached_sign_token: typing.Optional[str] = None
    _cache_expiry: typing.Optional[datetime] = None
    _cache_lock = asyncio.Lock()
    _cache_duration = timedelta(minutes=5)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    async def get_sign_token() -> str:
        async with httpx.AsyncClient() as client:
            req = await client.get("https://zonai.skport.com/api/v1/auth/refresh")
            sign_token = req.json()["data"]["token"]
            return sign_token

    @classmethod
    async def get_cached_sign_token(cls, force: bool) -> str:
        """
        获取缓存的签名密钥，支持自动重试和缓存机制
        - 缓存有效期1小时
        - 失败时自动重试3次
        - 线程安全
        """
        # 获取单例实例
        instance = cls()

        # 检查缓存是否有效
        if not force:
            async with instance._cache_lock:
                if instance._cached_sign_token and instance._cache_expiry and datetime.now() < instance._cache_expiry:
                    return instance._cached_sign_token

        # 缓存失效，需要重新获取
        retry_count = 0
        max_retries = 3
        sign_token = None

        while retry_count < max_retries:
            try:
                retry_count += 1
                sign_token = await instance.get_sign_token()
                break
            except Exception:
                if retry_count >= max_retries:
                    raise
                await asyncio.sleep(1)
        if not sign_token:
            return instance._cached_sign_token

        # 更新缓存
        async with instance._cache_lock:
            instance._cached_sign_token = sign_token
            instance._cache_expiry = datetime.now() + instance._cache_duration

        return sign_token
