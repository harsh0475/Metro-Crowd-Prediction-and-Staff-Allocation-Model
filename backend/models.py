from pydantic import BaseModel

class HourPredictionRequest(BaseModel):

    line: str

    date: str

    hour: int


class ShiftPredictionRequest(BaseModel):

    line: str

    date: str

    shift: str


class FestivalHourPredictionRequest(BaseModel):

    line: str

    date: str

    hour: int

    festival_name: str


class FestivalShiftPredictionRequest(BaseModel):

    line: str

    date: str

    shift: str

    festival_name: str