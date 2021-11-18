import uuid
import json
from src.core.settings import TOKEN
from src.entities import idUserSchema
from src.utils import getResponse

class Endpoint():
    def __init__(self) -> None:
        self.url = "https://msging.net"
        self.body = {}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        }

class IdDest():
    def __init__(self, endpoint:Endpoint, phone:str) -> None:
        self.endpoint = endpoint
        self.phone = phone
        self.endpoint.url = f"{endpoint.url}/commands"
        self.endpoint.body = {
            "id": f"{uuid.uuid4()}",
            "to": "postmaster@wa.gw.msging.net",
            "method": "get",
            "uri": f"lime://wa.gw.msging.net/accounts/{self.phone}"
        }
        self.id = ""  

    def parseResponse(self, response:dict) -> str:
        id_dest = (idUserSchema(**response)).dict()
        self.id = id_dest["resource"]["alternativeAccount"]

    def execute(self):
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
        return self.parseResponse(response.json())
