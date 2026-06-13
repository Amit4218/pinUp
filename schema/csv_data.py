from pydantic import BaseModel

class CsvData(BaseModel):
    circlename: str
    regionname: str
    divisionname: str
    officename: str
    pincode: str
    officetype: str
    delivery: str
    district: str
    statename: str
    latitude: float | str
    longitude: float | str