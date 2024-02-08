from schema.request_body import RequestBody
from schema.response_body import ResponseBody
from fastapi.encoders import jsonable_encoder
from starlette import status
from datetime import datetime
import re


async def xml_parse_process(request_body: RequestBody, http):
    request = jsonable_encoder(request_body)
    doc_date = request.get("doc_date", None)
    buyers = request.get("buyers", [])
    payments = request.get("payments", {})
    subject_agreement = request.get("SubjectAgreement", {})
    response = ResponseBody(doc_date=None, buyers=None, payments=None, SubjectAgreement=None)

    payments["СрокОплаты"] = convert_time_format(payments.get("СрокОплаты", ''))
    response.doc_date = format_date(doc_date)
    response.payments = payments
    response.SubjectAgreement = subject_agreement
    response.buyers = buyers
    return response


def format_date(input_date: str) -> str:
    date_pattern = r"(\d{1,2})\s*([а-яё]+)\s*(\d{4})"
    match = re.search(date_pattern, input_date, re.IGNORECASE)
    if match:
        day, month_str, year = match.groups()
        month_str = month_str.lower()
        months_dict = {
            'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
            'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
        }
        month = months_dict.get(month_str)
        if month:
            try:
                date_obj = datetime(int(year), month, int(day))
                formatted_date = date_obj.strftime("%d.%m.%Y")
                return formatted_date
            except ValueError:
                pass
    return ""


def convert_time_format(text):
    year = month = week = day = 0

    year_match = re.search(r'(\d+)\s*год*', text)
    month_match = re.search(r'(\d+)\s*месяц*', text)
    week_match = re.search(r'(\d+)\s*недел*', text)
    day_match = re.search(r'(\d+)\s*дне[йя]*', text)

    if year_match:
        year = int(year_match.group(1))
    if month_match:
        month = int(month_match.group(1))
    if week_match:
        week = int(week_match.group(1))
    if day_match:
        day = int(day_match.group(1))

    return f"{year}_{month}_{week}_{day}"
