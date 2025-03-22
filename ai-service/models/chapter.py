from pydantic import BaseModel
from typing import List, Dict, Any

class Chapter(BaseModel):
    id: str
    title: str
    chapter: str
    key_concepts: str
    topics: List[str]
    summary: str

