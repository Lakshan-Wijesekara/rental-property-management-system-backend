from dataclasses import dataclass

@dataclass
class User:
    firstname: str
    lastname: str
    propertyName: str
    email: str
    telephoneNumber: int 
    is_active : bool  