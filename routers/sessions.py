from fastapi import APIRouter, HTTPException
from typing import List

from functions.data.key import get_key_by_id
from functions.data.session import get_session_db

router = APIRouter()

@router.get("/key/{key_id}", response_model=List[dict])
def get_sessions_by_key(key_id: int):
    """
    Получить список сессий по ключу
    """
    key = get_key_by_id(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    sessions = get_session_db(key)
    return [
        {
            "id": s.id,
            "ip": s.ip,
            "connected": str(s.connected),
            "disconnected": str(s.disconnected),
            "total_bytes": s.total_bytes,
            "total_connected_time": s.total_connected_time
        }
        for s in sessions
    ]