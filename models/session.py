from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    key_id: int
    ip: str
    total_bytes: int
    total_connected_time: int
    connected: datetime
    disconnected: datetime

class SessionOut(SessionBase):
    id: int

    class Config:
        orm_mode = True