from typing import List, Optional
from pydantic import BaseModel
from Topic import Topic
import uuid

class Document(BaseModel):
    id: uuid.UUID
    name: str
    type: str
    file_path: str
    topics: Optional[List[Topic]] = []


