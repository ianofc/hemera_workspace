from pydantic import BaseModel

class UserEvent(BaseModel):
    user_id: str
    content_id: str
    event_type: str  # 'click', 'like', 'share', 'watch_time'
    value: float = 1.0