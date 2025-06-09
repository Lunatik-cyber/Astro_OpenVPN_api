from fastapi import APIRouter
from typing import Dict

from functions.data.key import (
    get_keys_db, get_keys_by_status_db, get_keys_by_connected_db,
    get_expired_keys_db, get_not_expired_keys_db, get_keys_by_config_db,
    get_keys_by_config_and_status_db, get_keys_by_config_and_connected_db,
    get_expired_keys_by_config_db, get_not_expired_keys_by_config_db,
)
from functions.data.configs import get_configs_db
from functions.data.session import (
    get_total_keys_bytes_db, get_total_key_bytes_by_config_db
)
from functions.other import math_bytes

router = APIRouter()

@router.get("/", response_model=Dict)
def statistics():
    """Общая статистика по ключам и конфигам"""
    total_keys = len(get_keys_db())
    total_keys_blocked = len(get_keys_by_status_db(False))
    total_keys_active = len(get_keys_by_status_db(True))
    total_keys_connected = len(get_keys_by_connected_db())
    total_keys_expired = len(get_expired_keys_db())
    total_keys_not_expired = len(get_not_expired_keys_db())
    total_configs = len(get_configs_db())
    total_traffic = math_bytes(get_total_keys_bytes_db())

    configs_stats = []
    for config in get_configs_db():
        configs_stats.append({
            "id": config.id,
            "port": config.port,
            "protocol": config.protocol,
            "address": config.address,
            "keys_total": len(get_keys_by_config_db(config.id)),
            "keys_active": len(get_keys_by_config_and_status_db(config.id, True)),
            "keys_blocked": len(get_keys_by_config_and_status_db(config.id, False)),
            "keys_connected": len(get_keys_by_config_and_connected_db(config.id, True)),
            "keys_expired": len(get_expired_keys_by_config_db(config.id)),
            "keys_not_expired": len(get_not_expired_keys_by_config_db(config.id)),
            "traffic": math_bytes(get_total_key_bytes_by_config_db(config.id)),
        })

    return {
        "total_keys": total_keys,
        "active_keys": total_keys_active,
        "blocked_keys": total_keys_blocked,
        "connected_keys": total_keys_connected,
        "expired_keys": total_keys_expired,
        "not_expired_keys": total_keys_not_expired,
        "total_configs": total_configs,
        "total_traffic": total_traffic,
        "configs": configs_stats
    }