from dataclasses import dataclass
from typing import Optional

@dataclass
class Property:
    selectedCity: str
    propertyName: str
    propertyArea: str
    monthlyRental: str
    latitude: str
    longtitude: str
    is_active: str