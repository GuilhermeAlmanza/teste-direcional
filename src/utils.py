from requests import post
import json

def getResponse(url_:str, headers_:dict, data_:dict) -> dict:
    try:
        request = post(url = url_, headers=headers_, data=json.dumps(data_))
        return request
    except:
        return {}