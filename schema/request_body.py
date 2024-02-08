from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    doc_date: str = Field(description="Дата документа")
    buyers: list = Field(description="Покупатели")
    payments: dict = Field(description="Данные о платежах и сроках")
    SubjectAgreement: dict = Field(description="Данные о договоре")