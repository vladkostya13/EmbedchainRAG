from pydantic import BaseModel


class UserInput(BaseModel):
    question: str


class DataSource(BaseModel):
    data_type: str
    data_value: str
