import traceback
from functools import wraps

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from schema.response_body import ErrorHandler


def try_execute_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            stack_trace = traceback.format_exc()
            data = {
                "errorText": stack_trace,
            }
            response = ErrorHandler.model_validate(data)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=jsonable_encoder(response),
            )

    return wrapper


class RequestError(Exception):
    def __init__(self, message: str, code: int) -> None:
        self.message = message
        self.code = code

    def __str__(self, *args, **kwargs):
        return self.message


class RequestErrorNotFound(RequestError):
    pass


class RequestErrorBadRequest(RequestError):
    pass


class RequestErrorServerError(RequestError):
    pass
