from pydantic import BaseModel
from typing import List, Dict, Any

class Document(BaseModel):
    id: str
    filename: str
    file_content: str
    metadata: str
    potential_chapters: List[Dict[str, Any]]
    