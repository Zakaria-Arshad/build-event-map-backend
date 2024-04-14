from pydantic import BaseModel, Field
from EventModel import Event
from typing import List

class Map(BaseModel):
    events: List[Event] = Field(default_factory=list) # makes empty list if submitted with nothing