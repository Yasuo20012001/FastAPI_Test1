import logging

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from endpoints import endpoints
from settings.config import settings
from settings.http_client import http_client

logging.basicConfig(level=logging.INFO)

"""Создаем фабрику приложения"""


class MyAppFactory:
    def __init__(self, settings, http_client):
        self.settings = settings
        self.app = FastAPI(
            title=self.settings.PROJECT_NAME,
            root_path=self.settings.WWW_DOMAIN if self.settings.config_name in ["DEV", "PROD"] else "",
            version=self.settings.VERSION,
            description=self.settings.DESCRIPTION,
            openapi_url="/%sec%openapi.json" if self.settings.config_name == "PROD" else "/openapi.json",
            docs_url="/%sec%docs" if self.settings.config_name == "PROD" else "/docs",
            redoc_url="/%sec%redoc" if self.settings.config_name == "PROD" else "/redoc",
            debug=True,
        )
        self.http_client = http_client

    async def startup_event(self):
        logger = logging.getLogger("uvicorn.access")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        file_handler_info = logging.FileHandler("uvicorn_info_log.log", mode="a")
        file_handler_info.setLevel(logging.INFO)
        logger.addHandler(file_handler_info)

        logger_error = logging.getLogger("uvicorn.error")
        file_handler_error = logging.FileHandler("uvicorn_error_log.log", mode="a")
        file_handler_error.setLevel(logging.ERROR)
        logger_error.addHandler(file_handler_error)

    async def http_startup(self):
        self.http_client.start()

    async def http_shutdown(self):
        await self.http_client.stop()

    def get_app(self) -> FastAPI:
        self.app.add_event_handler("startup", self.startup_event)

        routes = APIRouter()

        @routes.on_event("startup")
        async def startup():
            logging.info("Async session started.")
            await self.http_startup()

        @routes.on_event("shutdown")
        async def shutdown():
            logging.info("Closing async session.")
            await self.http_shutdown()

        routes.include_router(endpoints.router)

        self.app.include_router(routes)

        @self.app.exception_handler(RequestValidationError)
        async def custom_form_validation_error(request, exc):
            error_text = None
            for pydantic_error in exc.errors():
                loc, msg = pydantic_error["loc"], pydantic_error["msg"]
                filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc

                try:
                    field_string = ".".join([str(x) for x in filtered_loc])
                except Exception as e:
                    logging.error(f"An error occurred while formatting field string: {e}")
                    field_string = "unknown_field"

                # Создаем строку с ошибками
                error_str = f"{field_string}: {msg}"

                # Объединяем все ошибки в одну строку
                if error_text is None:
                    error_text = error_str
                else:
                    error_text += f"\n{error_str}"
            response_data = {
                "errorText": error_text,
            }

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=response_data,
            )
        return self.app


factory = MyAppFactory(settings, http_client=http_client)
app = factory.get_app()
