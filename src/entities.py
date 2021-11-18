from pydantic import BaseModel

class idUserSchema (BaseModel):
    resource:dict

class listTemplateSchema (BaseModel):
    resource:dict

class templateSchema (BaseModel):
    id:str
    components:list
    name:str