from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str = Field(...,min_length=3,max_length=50)
    email:EmailStr=Field(...)
    password: str = Field(...,min_length=6)
    admin_code: Optional[str]=None



class UserLoginSchema(BaseModel):
    email:EmailStr=Field(...)
    password: str =Field(...,min_length=6)