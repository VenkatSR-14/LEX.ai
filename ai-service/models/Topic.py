import uuid
from pydantic import BaseModel
from typing import List

class Topic:
    id: uuid.UUID
    document_id: uuid.UUID
    topic_name: str
    topic_description: str