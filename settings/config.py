import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import AnyHttpUrl

load_dotenv()


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0", "*"]
    PROJECT_NAME: str = "XML PARSER APP"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "XML parser app"
    WWW_DOMAIN = "/api/dms/test-xmlparser-app"


class DevelopmentConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")


class ProductionConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "PROD")


class LocalConfig(BaseConfig):
    config_name = os.environ.get("FASTAPI_CONFIG", "LOCAL")


@lru_cache
def get_settings():
    config_cls_dict = {
        "DEV": DevelopmentConfig,
        "PROD": ProductionConfig,
        "LOCAL": LocalConfig,
    }
    config_name = os.environ.get("FASTAPI_CONFIG", "DEV")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
