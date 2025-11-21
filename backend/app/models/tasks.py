from pydantic import BaseModel,Field
from typing import Optional

class TaskCreateSchema(BaseModel):
    title: str =Field(...,min_length=3)
    description: str = Field(...)
    completed: bool = False
class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None