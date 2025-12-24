from pydantic import BaseModel

class Contact(BaseModel):
    first_name:str
    last_name:str
    phone_number:str