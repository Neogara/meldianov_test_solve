from pydantic import BaseModel


class ConvertRatesModel(BaseModel):
    code_from: str
    code_to: str
    value: float


class ConvertRatesReturnModel(BaseModel):
    result: float
