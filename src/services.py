from aiohttp.helpers import BasicAuth
from core.settings import logger
from dtos import SMSBody
from aiohttp import ClientSession

import asyncio
from typing import Any, AsyncGenerator
from aiohttp import ClientSession
from urllib.parse import urlparse
from functools import cache


class SessionManager:
    def __init__(self, *, delay: bool):
        self.loaded = False
        if not delay:
            self.init()

    def init(self):
        if self.loaded: return
        self.clients: dict[str, ClientSession] = {}
        self.get_client("http://default")
        self.loaded = True

    def get_client(self, url: str):
        name = urlparse(url).netloc
        if client := self.clients.get(name):
            return client
        self.clients[name] = ClientSession()
        return self.clients[name]

    async def request(self, method: str, url: str, **kwargs):
        async with self.get_client(url).request(method, url, **kwargs) as response:
            yield await response.json(encoding="utf8")

    def get(self, url: str, *, params: dict[str, Any] = {}, **kwargs):
        return self.request("GET", url, params=params, **kwargs)

    def post(
        self,
        url: str,
        *,
        json: dict[str, Any] = {},
        data: dict[str, Any] = {},
        **kwargs,
    ):
        if json:
            return self.request("POST", url, json=json, **kwargs)
        else:
            return self.request("POST", url, data=data, **kwargs)

    async def finish(self):
        await asyncio.gather(*[value.close() for value in self.clients.values()])


session_manager = SessionManager(delay=True)


async def send_single_sms(
    client: SessionManager, data: SMSBody
) -> AsyncGenerator[dict, None]:
    logger.info(data.dict(by_alias=True))
    async for response in client.post(
        "https://sms-api-pointer.pontaltech.com.br/v1/single-sms",
        json=data.dict(by_alias=True),
        auth=BasicAuth(login="blu365salesforcepremium", password="1CwF41cMTc"),
    ):
        yield response