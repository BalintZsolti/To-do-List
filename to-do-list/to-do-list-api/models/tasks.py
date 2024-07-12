from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    id: Optional[str] = Field(default_factory=str)
    title: str
    description: str
    status: str
