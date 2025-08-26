from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Pydantic models
class ChatMessage(BaseModel):
    query: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    response: Any
    conversation_id: str
    timestamp: datetime
    sources: List[Dict[str, Any]]