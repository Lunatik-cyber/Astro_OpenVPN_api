from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Pydantic models
class KeyCreateRequest(BaseModel):
    name: str
    days: int
    amount: int = 1
    config_id: int
    email: Optional[str] = None

class KeyEditRequest(BaseModel):
    days: Optional[int] = None
    email: Optional[str] = None

class TransferKeyRequest(BaseModel):
    config_id: int

class BlockBulkRequest(BaseModel):
    ids: List[int]

class MailBulkRequest(BaseModel):
    ids: List[int]
    email: Optional[str] = None

class ActionBulkRequest(BaseModel):
    ids: List[int]