from fastapi.param_functions import Depends
from starlette.requests import Request
from starlette.responses import Response
from controllers import Controller
from database.repositories.api_message import APIMessageRepository
from database.repositories.callback import CallbackRepository
from database.repositories.reply import ReplyRepository
from dtos import APIMessageDTO, APIReplyDTO, CallbackBodyDTO
from starlette.status import HTTP_204_NO_CONTENT

api_message_repository = APIMessageRepository()
reply_repository = ReplyRepository()
callback_repository = CallbackRepository()

class CallbacksController(Controller):
    def include_routes(self):
        self.router.post(
            "/listen",
            status_code=HTTP_204_NO_CONTENT,
            name="Callback Listener",
            dependencies=[Depends(self.middleware)]
        )(self.listen_to_callback)
        
    async def middleware(self, request: Request):
        print(await request.body())
        print(await request.json())

    async def listen_to_callback(self, data: CallbackBodyDTO):
        callback_id = callback_repository.create(data)
        if isinstance(data, APIMessageDTO):
            self.process_api_message(data, callback_id)
        else:
            self.process_api_reply(data, callback_id)
        return Response(status_code=HTTP_204_NO_CONTENT)

    def process_api_message(self, data: APIMessageDTO, callback_id: int):
        api_message_repository.create(data, callback_id)

    def process_api_reply(self, data: APIReplyDTO, callback_id: int):
        reply_repository.create_many(data.replies, callback_id)