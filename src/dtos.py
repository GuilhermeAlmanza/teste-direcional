import re
from typing import Any, Optional, Union
from pydantic import BaseModel
from datetime import datetime
from pydantic.class_validators import validator
from pydantic.fields import Field

phone_regexp = re.compile(r"^55")
camel_case_regexp = re.compile("_([a-zA-Z])")


class DTO(BaseModel):
    class Config:
        alias_generator = lambda string: re.sub(
            camel_case_regexp, lambda match: match[1].upper(), string
        )
        allow_population_by_field_name = True
        extra = "allow"


class InArgumentDTO(DTO):
    phone: Optional[str] = None

    @validator("phone")
    def phone_parse(cls, value: str):
        if len(value) <= 11:
            return value
        return re.sub(phone_regexp, "", value)


class DataDTO(DTO):
    in_arguments: list[InArgumentDTO]
    key_value: Optional[str] = None
    message: str
    mode: Optional[str] = None
    journey_id: str


class SMSBody(DTO):
    to: str
    message: str
    url_callback: str = "https://pontal-blu.loca.lt/api/listen"
    reference: str = "Default"

class APIMessageDTO(DTO):
    type: str = "api_message"
    id: str
    to: str
    message: str
    schedule: datetime
    reference: str
    status: str
    status_description: str

    class Config:
        schema_extra = {
            "examples": [
                {
                    "type": "api_message",
                    "id": "1394547",
                    "to": "11999762022",
                    "message": "mensagem",
                    "schedule": "2016-08-12T15:16:20Z",
                    "reference": "",
                    "status": "2",
                    "statusDescription": "Queued",
                },
                {
                    "type": "api_reply",
                    "replies": [
                        {
                            "messageId": "1394547",
                            "mailingId": "2152412",
                            "mailingName": "SMS1510_CSF_DIG",
                            "reference": "",
                            "classify": "",
                            "value": "0.00",
                            "message": "Ok",
                            "received": "2016-08-12 15:18:03",
                            "from": "11999762022",
                            "accountId": "123",
                            "accountName": "teste",
                            "vars": {},
                        }
                    ],
                },
            ]
        }


class ReplyDTO(DTO):
    message_id: str
    mailing_id: str
    mailing_name: str
    reference: str
    classify: str
    value: str
    message: str
    received: datetime
    from_: str = Field(..., alias="from")
    account_id: str
    account_name: str
    vars: dict[str, Any] = {}


class APIReplyDTO(DTO):
    type: str = "api_reply"
    replies: list[ReplyDTO]


CallbackBodyDTO = Union[APIMessageDTO, APIReplyDTO]