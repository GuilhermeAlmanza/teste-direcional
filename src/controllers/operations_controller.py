import re
from src.controllers import Controller
from src.core.settings import logger
from src.dtos import DataDTO, InArgumentDTO, MessageBody, SMSBody, APIMessageDTO
from src.services import send_single_sms, session_manager
from src.retrieve_user import Endpoint, IdDest
from src.trigger import Trigger
from src.redirect_flow import RedirectFlow

placeholder_regexp = re.compile(r"<<[a-zA-Z]+>>")
field_name_regexp = re.compile(r"[a-zA-Z]+")


class OperationsController(Controller):
    def include_routes(self):
        #self.router.post("/data", name="receive data")(self.receive_data)
        self.router.post("/data", name="receive data")(self.rec_data)
        self.router.post("/save", response_model=None, name="save")(self.save)
        self.router.post("/validate", response_model=None, name="validate")(
            self.validate
        )
        self.router.post("/publish", response_model=None, name="publish")(self.publish)
        self.router.post("/stop", response_model=None, name="stop")(self.stop)

    def _log_handler(self, operation_name: str):
        logger.info(f"Received operation: {operation_name}")

    def save(self):
        self._log_handler("save")

    def validate(self):
        self._log_handler("validate")

    def publish(self):
        self._log_handler("publish")

    def stop(self):
        self._log_handler("stop")

    @staticmethod
    def log_data(phone: str, journey: str):
        logger.info(f"Received data from {phone} in journey {journey}")
    
    async def receive_data(self, data:dict):

        async for response in send_single_sms(
            session_manager,
            SMSBody(
                telephone=data['keyValue'],
                message="",
                reference=data["journeyId"],
                metadata=data["metadata"]
            ),
        ):
            pass
        
        return True

    def rec_data(self, data:dict):
        try:
            self.execute(
                MessageBody(
                    telephone=data['keyValue'],
                    message="",
                    reference=data['journeyId'],
                    metadata=data['metadata']
                )
            )
            return True
        except:
            return False

        
    def get_message(self, data: DataDTO):
        message = data.message
        matches = re.findall(placeholder_regexp, message)
        if matches:
            for match in matches:
                field_name = self.get_field_name(match)
                message = message.replace(
                    match, self.get_in_argument(data.in_arguments, field_name)
                )
        return message

    @staticmethod
    def get_field_name(matched_item: str):
        match = re.search(field_name_regexp, matched_item)
        if match:
            return match[0]
        return ""

    @staticmethod
    def get_in_argument(
        in_arguments: list[InArgumentDTO], field: str, optional: str = ""
    ) -> str:
        for item in in_arguments:
            result = getattr(item, field, "")
            if result and "Event." not in result:
                return result
        return optional

    def execute(self, data:dict):
        endpoint = Endpoint()
        data = dict(data)
        print(data)
        get_client = IdDest(endpoint, data['telephone'])
        get_client.execute()
        print(get_client.id)

        trigger = Trigger(endpoint, get_client.id, data['metadata']['idtemplate'])
        response = trigger.execute()
        print(response)

        redirect_flow = RedirectFlow(endpoint, 
                                     get_client.id, 
                                     data['metadata']['idsubbot'],
                                     data['metadata']['idfluxo'],
                                     data['metadata']['idbloco'])
        status = redirect_flow.execute()
        print(status)