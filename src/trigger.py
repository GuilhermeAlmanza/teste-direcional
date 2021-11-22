import uuid
import json
from src.retrieve_user import Endpoint
from src.utils import getResponse

class Trigger():
    def __init__(self, endpoint:Endpoint, id_account, id_template, name_template) -> None:
        self.endpoint = endpoint
        self.id_account = id_account
        self.id_template = id_template
        self.name_template = name_template

    def setBody(self):
        self.endpoint.url = "https://msging.net/messages"
        self.endpoint.body = {
            "id":f"{uuid.uuid4()}",
            "to":f"{self.id_account}",
            "type":"application/json",
            "content":{
                "type":"template",
                "template":{
                    "namespace":f"{self.id_template}",
                    "name":f"{self.template_name}",
                    "language":{
                        "code":"pt_BR",
                        "policy":"deterministic"
                    }
                }
            }    
        }

    def messageTrigger(self):
        print(self.endpoint.url)
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
        if response:
            print(response)
            return response
        else: 
            print("deu ruim")
            return None

    def execute(self):
        if self.id_account == None:
            return
        else: 
            self.setBody()
            return self.messageTrigger()