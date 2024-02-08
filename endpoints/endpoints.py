from fastapi import APIRouter, Depends
from starlette import status

from error_handler.error_handler import RequestErrorServerError
from error_handler.error_handler import try_execute_async
from schema.error_message import RequestErrorMessages
from schema.request_body import RequestBody
from schema.response_body import ResponseBody
from service.services import xml_parse_process
from settings import HttpClient, get_http_client

router = APIRouter()


@router.get("/health")
async def test_api():
    return {"status_code": status.HTTP_200_OK}


@router.post(path="/xml_parse_app", response_model=ResponseBody, responses={400: {"model": ResponseBody}})
@try_execute_async
async def xml_parse_app(request_body: RequestBody, http_client: HttpClient = Depends(get_http_client)):
    if not isinstance(request_body, RequestBody):
        raise RequestErrorServerError(code=400, message=f"{RequestErrorMessages.ResponseDoesNotCorrect}")

    return await xml_parse_process(request_body=request_body, http=http_client)
