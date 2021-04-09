import re
from controllers import Controller
from core.settings import logger
from dtos import DataDTO, InArgumentDTO, SMSBody, APIMessageDTO
from services import send_single_sms, session_manager
from database.repositories.api_message import APIMessageRepository

placeholder_regexp = re.compile(r"<<[a-zA-Z]+>>")
field_name_regexp = re.compile(r"[a-zA-Z]+")

api_message_repository = APIMessageRepository()


class OperationsController(Controller):
    def include_routes(self):
        self.router.post("/data", name="receive data")(self.receive_data)
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

    async def receive_data(self, data: DataDTO):
        phone = self.get_in_argument(data.in_arguments, "phone", "user")
        self.log_data(phone, data.journey_id)
        async for response in send_single_sms(
            session_manager,
            SMSBody(
                to=phone,
                message=self.get_message(data),
                reference=data.journey_id,
            ),
        ):
            api_message_repository.create(APIMessageDTO.parse_obj(response))

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