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
        self.endpoint.url = "https://http.msging.net/messages"
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
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
        print(response)
        if response:
            return response
        else: return None

    def execute(self):
        if self.id_account == None:
            print("self id == none")
            return
        else: 
            self.setBody()
            return self.messageTrigger()