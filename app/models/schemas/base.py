from datetime import datetime, timezone

from pydantic import BaseModel, BaseConfig


def convert_datetime(dt: datetime) -> str:
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {datetime: convert_datetime}
        alias_generator = convert_field_to_camel_case
