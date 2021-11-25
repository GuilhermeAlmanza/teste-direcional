from src.retrieve_user import Endpoint, IdDest
from src.trigger import Trigger
from src.redirect_flow import RedirectFlow
from aiohttp import ClientSession

import asyncio
import jwt 
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

def send_whatsapp(data:dict):
    print("executing...")
    endpoint = Endpoint()
    data = dict(data)
    get_client = IdDest(endpoint, data['telephone'])
    get_client.execute()
    print(get_client.id)

    trigger = Trigger(endpoint, get_client.id, data['metadata']['idtemplate'], data['metadata']['nametemplate'])
    response = trigger.execute()
    print(response)

    redirect_flow = RedirectFlow(endpoint, 
                                    get_client.id, 
                                    data['metadata']['idsubbot'],
                                    data['metadata']['idfluxo'],
                                    data['metadata']['idbloco'])
    status = redirect_flow.execute()
    print(status)