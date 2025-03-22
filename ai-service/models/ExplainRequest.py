from pydantic import BaseModel
import univorn
from typing import Optional

class ExplainRequest(BaseModel):
    text: str
    context: Optional[str] = ""
