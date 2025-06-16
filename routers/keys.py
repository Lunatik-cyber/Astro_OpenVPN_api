from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

from api.models.key import (
    ActionBulkRequest, 
    KeyCreateRequest, 
    KeyEditRequest, 
    TransferKeyRequest,
    KeyOut)
from functions.data.key import (
    get_key_by_id, get_keys_by_name_db, edit_key_db
) 
from functions.list import KeysList
from functions.client import (
    create_key, delete_key, renew_key, recreate_key, block_key, unblock_key, transfer_key
)
from functions.data.session import get_session_db, delete_session_db
from functions.other import key_to_tg, key_to_email
from functions.data.settings import get_settings_db

router = APIRouter()


@router.get("/", response_model=List[KeyOut])
def list_keys(
    by: Optional[str] = Query(
        "all",
        description=(
            "Критерий фильтрации ключей: "
            "all, name, email, status, port, config, protocol, days, date, created, updated, "
            "expired, expired_days, traffic, sessions, connected_time, free_keys"
        )
    ),
    value: Optional[str] = Query(
        None,
        description="Значение фильтра (например, имя, email, порт, id конфига, статус и т.д.)"
    ),
):
    """
    Получить список ключей с возможностью фильтрации.

    **Фильтры:**
    - by=all (default) — все ключи
    - by=name&value=NAME — по имени
    - by=email&value=EMAIL — по email
    - by=status&value=true/false — по статусу
    - by=port&value=PORT — по порту
    - by=config&value=CONFIG_ID — по ID конфига
    - by=protocol&value=udp/tcp — по протоколу
    - by=days&value=30 — по количеству дней
    - by=created/updated/date&value=YYYY-MM-DD — по дате создания/обновления
    - by=expired — все истекшие
    - by=expired_days — все, отсортированные по дате истечения
    - by=traffic — сортировка по трафику
    - by=sessions — сортировка по количеству сессий
    - by=connected_time — сортировка по времени подключения
    - by=free_keys — только свободные ключи
    """
    def parse_value(criteria, value):
        if value is None:
            return None
        if criteria in ["port", "days", "config"]:
            try:
                return int(value)
            except Exception:
                return value
        if criteria in ["status"]:
            v = value.lower()
            if v in ("true", "1", "yes", "on"):
                return True
            if v in ("false", "0", "no", "off"):
                return False
            return value
        return value

    parsed_value = parse_value(by, value)
    keys = KeysList.list_by_criteria(by, parsed_value)
    return keys


@router.get("/{key_id}", response_model=dict)
def key_info(key_id: int):
    """
    Получить подробную информацию по ключу по его ID.
    """
    key = get_key_by_id(key_id)
    if key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return KeysList.default_json(1, key)


@router.post("/", response_model=dict)
def create_key_api(data: KeyCreateRequest):
    """
    Создать новый ключ или несколько ключей.  
    В ответе — первый созданный ключ.
    """
    create_key(data.name, data.days, data.amount, data.config_id, data.email)
    keys = get_keys_by_name_db(data.name)
    return KeysList.default_json(1, keys[0])


@router.delete("/{key_id}")
def delete_key_api(key_id: int):
    """
    Удалить ключ по его ID.
    """
    delete_key(key_id)
    return {"result": "deleted"}


@router.put("/{key_id}", response_model=dict)
def edit_key_api(key_id: int, data: KeyEditRequest):
    """
    Изменить срок действия или email у ключа по ID.
    """
    key = get_key_by_id(key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    days = data.days if data.days is not None else key.days
    email = data.email if data.email is not None else key.email
    edit_key_db(name=key.name, days=days, email=email)
    return KeysList.default_json(1, get_key_by_id(key_id))


@router.post("/{key_id}/block")
def block_key_api(key_id: int):
    """
    Заблокировать ключ (по ID).
    """
    key = get_key_by_id(key_id)
    block_key(key)
    return {"result": "blocked"}


@router.post("/{key_id}/unblock")
def unblock_key_api(key_id: int):
    """
    Разблокировать ключ (по ID).
    """
    key = get_key_by_id(key_id)
    unblock_key(key)
    return {"result": "unblocked"}


@router.post("/{key_id}/recreate")
def recreate_key_api(key_id: int):
    """
    Пересоздать ключ (по ID).
    """
    recreate_key(key_id)
    return {"result": "recreated"}


@router.post("/{key_id}/renew")
def renew_key_api(key_id: int, days: int = Body(...)):
    """
    Продлить ключ на N дней (по ID).
    """
    renew_key(key_id, days)
    return {"result": "renewed"}


@router.post("/{key_id}/transfer")
def transfer_key_api(key_id: int, data: TransferKeyRequest):
    """
    Перенести ключ на другой конфиг (по ID ключа и ID нового конфига).
    """
    transfer_key(key_id, data.config_id)
    return {"result": "transferred"}


@router.get("/{key_id}/sessions", response_model=List[dict])
def key_sessions_api(key_id: int):
    """
    Получить список сессий по ключу (по ID ключа).
    """
    sessions = get_session_db(get_key_by_id(key_id))
    return [
        {
            "id": s.id,
            "ip": s.ip,
            "connected": s.connected,
            "disconnected": s.disconnected,
            "total_bytes": s.total_bytes,
            "total_connected_time": s.total_connected_time
        }
        for s in sessions
    ]


@router.post("/{key_id}/send_tg")
def send_key_to_tg_api(key_id: int):
    """
    Отправить ключ в Telegram (по ID ключа, настройки берутся из settings).
    """
    key = get_key_by_id(key_id)
    key_to_tg(key, get_settings_db())
    return {"result": "sent"}


@router.post("/{key_id}/send_mail")
def send_key_to_mail_api(key_id: int):
    """
    Отправить ключ на почту (по ID ключа, настройки берутся из settings).
    """
    key = get_key_by_id(key_id)
    key_to_email(key, get_settings_db())
    return {"result": "sent"}


@router.post("/{key_id}/fix")
def fix_key_api(key_id: int):
    """
    Принудительно отключить ключ (фиксировать статус connected=False).
    """
    key = get_key_by_id(key_id)
    edit_key_db(name=key.name, connected=False)
    return {"result": "fixed"}


@router.post("/bulk/block")
def block_keys_bulk_api(data: ActionBulkRequest):
    """
    Заблокировать список ключей (bulk).
    """
    for key_id in data.ids:
        key = get_key_by_id(key_id)
        if key:
            block_key(key)
    return {"result": "blocked_bulk"}


@router.post("/bulk/unblock")
def unblock_keys_bulk_api(data: ActionBulkRequest):
    """
    Разблокировать список ключей (bulk).
    """
    for key_id in data.ids:
        key = get_key_by_id(key_id)
        if key:
            unblock_key(key)
    return {"result": "unblocked_bulk"}


@router.post("/bulk/send_tg")
def send_keys_to_tg_bulk_api(data: ActionBulkRequest):
    """
    Отправить несколько ключей в Telegram (bulk).
    """
    for key_id in data.ids:
        key = get_key_by_id(key_id)
        if key:
            key_to_tg(key, get_settings_db())
    return {"result": "sent_bulk"}


@router.post("/bulk/send_mail")
def send_keys_to_mail_bulk_api(data: ActionBulkRequest):
    """
    Отправить несколько ключей на почту (bulk).
    """
    for key_id in data.ids:
        key = get_key_by_id(key_id)
        if key:
            key_to_email(key, get_settings_db())
    return {"result": "sent_bulk"}


@router.post("/bulk/delete")
def delete_keys_bulk_api(data: ActionBulkRequest):
    """
    Удалить несколько ключей (bulk).
    """
    for key_id in data.ids:
        delete_key(key_id)
    return {"result": "deleted_bulk"}


@router.post("/bulk/fix")
def fix_keys_bulk_api(data: ActionBulkRequest):
    """
    Принудительно отключить несколько ключей (bulk).
    """
    for key_id in data.ids:
        key = get_key_by_id(key_id)
        if key:
            edit_key_db(name=key.name, connected=False)
    return {"result": "fixed_bulk"}


@router.post("/bulk/clear_traffic")
def clear_traffic_keys_bulk_api(data: ActionBulkRequest):
    """
    Очистить трафик (сессии) по нескольким ключам (bulk).
    """
    for key_id in data.ids:
        delete_session_db(key_id)
    return {"result": "cleared_bulk"}