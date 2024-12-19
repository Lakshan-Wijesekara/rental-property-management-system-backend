from pydantic import BaseModel

class Property(BaseModel):
    selectedCity: str
    propertyName: str
    propertyArea: str
    monthlyRental: str
    latitude: str
    longtitude: str
    is_active: True
