from aiohttp.helpers import BasicAuth
from src.core.settings import logger
from src.dtos import SMSBody
from aiohttp import ClientSession

import asyncio
import jwt 
from typing import Any, AsyncGenerator
from aiohttp import ClientSession
from urllib.parse import urlparse
from functools import cache
from src.core.settings import SECRET_SMOOCH,APP_ID_SMOOCH,ID_INTEGRATION_WHATSAPP_SMOOCH,ID_SMOOCH


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


async def send_single_sms(client: SessionManager, data: SMSBody) -> AsyncGenerator[dict, None]:

    logger.info(data.dict(by_alias=True))
    async for response in client.post(
        "https://api.smooch.io/v1.1/apps/"+f"{ID_SMOOCH}/"+"notifications",
        json=return_body_whatsapp(data.dict()),
        headers={"Content-Type":"application/json","Authorization":jwt_smooch_bearer()},
    ):
        yield response


def jwt_smooch_bearer():

    '''
        Retorna o JWT(Bearer token) para chamadas no smooch do cliente
    '''

    return 'Bearer ' + str(jwt.encode({'scope': 'app'}, SECRET_SMOOCH, algorithm='HS256', headers={'kid': APP_ID_SMOOCH}))


def return_body_whatsapp(data:dict):
    return {

        "destination":{
            "integrationId":f"{ID_INTEGRATION_WHATSAPP_SMOOCH}",
            "destinationId":f"{data['telephone']}"
        },
        "author":{
            "role":"appMaker"
        },
        "messageSchema":"whatsapp",
        "message":{
            "type":"template",
            "template":{
                "namespace":f"{data['metadata']['namespace']}",
                "name":f"{data['metadata']['nametemplate']}",
                "language":{
                    "policy":"deterministic",
                    "code":"pt_BR"
                },
                "components":[
                    {
                    "type":"header",
                    "parameters":[
                        {
                            "type":"image",
                            "image":{
                                "link":f"{data['metadata']['image']}"
                            }
                        }
                    ]
                    }
                ]
            }
        }
        }