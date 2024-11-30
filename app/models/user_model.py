from pydantic import BaseModel

class User(BaseModel):
    firstname: str
    lastname: str
    propertyName: str
    email: str
    telephoneNumber: int 
    is_active : bool  