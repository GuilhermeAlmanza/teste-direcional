import uuid
import json
from src.retrieve_user import Endpoint
from src.entities import templateSchema, listTemplateSchema
from src.utils import getResponse

class Trigger():
    def __init__(self, endpoint:Endpoint, id_account, id_template) -> None:
        self.endpoint = endpoint
        self.id_account = id_account
        self.id_template = id_template
        self.components = {}
        self.template_name=""


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
                    },
                    "components":[f"{self.components}"]
                }
            }    
        }

    def selectTemplate(self, list_templates:list):
        for template in list_templates:
            if template["id"] == self.id_template:
                self.components = template["components"][0]
                self.template_name = template["name"]

    def setTemplates(self, response):
        dict_response = (listTemplateSchema(**response)).dict()
        list_response = dict_response["resource"]["data"]
        list_templates = []
        for template in list_response:
            data = (templateSchema(**template)).dict()
            list_templates.append(data)
        return list_templates

    def getTemplates(self):
        body_templates = {   
            "id": f"{uuid.uuid4()}", 
            "to": "postmaster@wa.gw.msging.net", 
            "method": "get", 
            "uri": "/message-templates" 
        }
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=body_templates)
        return response.json()

    def messageTrigger(self):
        response = getResponse(url_=self.endpoint.url, headers_=self.endpoint.headers, data_=self.endpoint.body)
        if response:
            return response
        else: return None

    def execute(self):
        response = self.getTemplates()
        list_templates = self.setTemplates(response)
        self.selectTemplate(list_templates)
        if self.id_account == None:
            return
        else: 
            self.setBody()
            return self.messageTrigger()