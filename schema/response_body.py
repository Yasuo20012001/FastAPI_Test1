from typing import Optional

from pydantic import BaseModel, Field


class ResponseBody(BaseModel):
    doc_date: Optional[str] = Field(description="Дата документа")
    buyers: Optional[list] = Field(description="Покупатели")
    payments: Optional[dict] = Field(description="Данные о платежах и сроках")
    SubjectAgreement: Optional[dict] = Field(description="Данные о договоре")


class ErrorHandler(BaseModel):
    errorText: Optional[str] = Field(description="Ошибка сервиса")