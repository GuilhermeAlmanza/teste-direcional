import uuid
import json
from src.utils import getResponse
from src.retrieve_user import Endpoint


class RedirectFlow():
    def __init__(self, endpoint:Endpoint, id_user:str, id_sub_bot:str, id_fluxo:str, id_bloco:str) -> None:
        self.endpoint = endpoint
        self.endpoint.url = "https://msging.net/commands"
        self.id_user = id_user
        self.id_sub_bot = id_sub_bot
        self.id_fluxo = id_fluxo
        self.id_bloco = id_bloco

    def setBodyMasterState(self):
        self.endpoint.body = {
            "id": f"{uuid.uuid4()}",
            "to": "postmaster@msging.net",
            "method": "set",
            "uri": f"/contexts/{self.id_user}/Master-State",
            "type": "text/plain",
            "resource": f"{self.id_sub_bot}@msging.net"
        }

    def setBodyRoute(self):
        self.endpoint.body = {
            "id": f"{uuid.uuid4()}",
            "to": "postmaster@msging.net",
            "method": "set",
            "uri": f"/contexts/{self.id_user}/stateid%40{self.id_fluxo}",
            "type": "text/plain",
            "resource": f"{self.id_bloco}"
        }

    def getStatus(self, request):
        status = request["status"]
        if status == "success":
            return True
        else: return False

    def execute(self):
        self.setBodyMasterState()
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
        status_master = self.getStatus(response.json())
        print(f"status master state: {status_master}")
        if status_master:
            self.setBodyRoute()
            response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
            status = self.getStatus(response.json())
            if status:
                print(f"status new route: {status}")
                return True
            else: return False
        else: return False
