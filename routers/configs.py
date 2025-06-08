from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel

from functions.data.configs import (
    get_configs_db, get_config_by_id_db, create_config_db, delete_config_db,
)
from functions.server_control import (
    disable_config_db, enable_config_db, restart_config_db
)
from functions.data.key import get_keys_by_config_db
from functions.list import KeysList

router = APIRouter()

class ConfigCreateRequest(BaseModel):
    port: int
    protocol: str
    address: str
    subnet: str
    telnet_port: Optional[int] = None

@router.get("/", response_model=List[dict])
def list_configs():
    """Список всех конфигураций"""
    configs = get_configs_db()
    return [
        {
            "id": c.id,
            "port": c.port,
            "protocol": c.protocol,
            "telnet_port": c.telnet_port,
            "address": c.address,
            "subnet": c.subnet,
            "status": c.status,
            "created": str(c.created),
            "updated": str(c.updated)
        }
        for c in configs
    ]

@router.get("/{config_id}", response_model=dict)
def get_config(config_id: int):
    """Получить инфу о конфиге"""
    c = get_config_by_id_db(config_id)
    if not c:
        raise HTTPException(status_code=404, detail="Config not found")
    return {
        "id": c.id,
        "port": c.port,
        "protocol": c.protocol,
        "telnet_port": c.telnet_port,
        "address": c.address,
        "subnet": c.subnet,
        "status": c.status,
        "created": str(c.created),
        "updated": str(c.updated)
    }

@router.post("/", response_model=dict)
def create_config(data: ConfigCreateRequest):
    """Создать конфиг OpenVPN"""
    telnet_port = data.telnet_port if data.telnet_port else 9999  # либо рандом
    create_config_db(
        port=data.port,
        protocol=data.protocol,
        telnet_port=telnet_port,
        subnet=data.subnet,
        address=data.address
    )
    c = get_configs_db()[-1]
    return {
        "id": c.id,
        "port": c.port,
        "protocol": c.protocol,
        "telnet_port": c.telnet_port,
        "address": c.address,
        "subnet": c.subnet,
        "status": c.status,
        "created": str(c.created),
        "updated": str(c.updated)
    }

@router.delete("/{config_id}")
def delete_config(config_id: int):
    """Удалить конфиг"""
    delete_config_db(config_id)
    return {"result": "deleted"}

@router.post("/{config_id}/disable")
def disable_config(config_id: int):
    """Отключить конфиг (systemctl stop ...)"""
    disable_config_db(config_id)
    return {"result": "disabled"}

@router.post("/{config_id}/enable")
def enable_config(config_id: int):
    """Включить конфиг (systemctl start ...)"""
    enable_config_db(config_id)
    return {"result": "enabled"}

@router.post("/{config_id}/restart")
def restart_config(config_id: int):
    """Перезапустить конфиг (systemctl restart ...)"""
    restart_config_db(config_id)
    return {"result": "restarted"}

@router.get("/{config_id}/keys", response_model=List[dict])
def config_keys(config_id: int):
    """Ключи, относящиеся к конфигу"""
    keys = get_keys_by_config_db(config_id)
    return [KeysList.default_json(i + 1, k) for i, k in enumerate(keys)]