from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ExplainRequest(BaseModel):
    text: str
    context: Optional[str] = ""
    chapter_id: Optional[str] = None
    
class ChapteAnalysisRequest(BaseModel):
    text: str
    document_type: str = "textbook"
    
# Used for matching syllabus to the textbook.
class MatchRequest(BaseModel):
    textbook_chapters :List[Dict[str, Any]]
    syllabus_topics :List[Dict[str, Any]]
    
    
    