from dataclasses import dataclass

@dataclass
class Property:
    selectedCity: str
    propertyName: str
    propertyArea: str
    monthlyRental: str
    latitude: str
    longtitude: str
    is_active: True
