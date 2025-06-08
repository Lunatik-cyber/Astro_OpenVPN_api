from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict
from pydantic import BaseModel

from functions.data.settings import get_settings_db
from functions.other import load_mail_settings, save_mail_settings
import subprocess

router = APIRouter()


class BotSettingsRequest(BaseModel):
    bot_token: Optional[str] = None
    bot_chat_id: Optional[str] = None

class MailSettingsRequest(BaseModel):
    use_mail: Optional[bool] = None
    mail_host: Optional[str] = None
    mail_port: Optional[int] = None
    mail_login: Optional[str] = None
    mail_password: Optional[str] = None

class MailNotifySettingsRequest(BaseModel):
    mail_create_key: Optional[bool]
    mail_delete_key: Optional[bool]
    mail_expired_key: Optional[bool]
    mail_block_key: Optional[bool]
    mail_unblock_key: Optional[bool]
    mail_day_before_expired: Optional[bool]
    mail_week_before_expired: Optional[bool]
    mail_update_key: Optional[bool]
    mail_renew_key: Optional[bool]
    mail_transfer_key: Optional[bool]
    mail_traffic_limit: Optional[bool]

@router.get("/", response_model=Dict)
def get_settings():
    """Получить все настройки бота и почты"""
    s = get_settings_db()
    mail_settings = load_mail_settings()
    return {
        "bot_token": s.bot_token,
        "bot_chat_id": s.bot_chat_id,
        "use_mail": s.use_mail,
        "mail_host": s.mail_host,
        "mail_port": s.mail_port,
        "mail_login": s.mail_login,
        "mail_password": s.mail_password,
        "mail_notify": mail_settings
    }

@router.put("/bot", response_model=Dict)
def update_bot_settings(data: BotSettingsRequest):
    """Обновить настройки бота"""
    s = get_settings_db()
    if data.bot_token is not None:
        s.bot_token = data.bot_token
    if data.bot_chat_id is not None:
        s.bot_chat_id = data.bot_chat_id
    s.save()
    return {"result": "updated", "bot_token": s.bot_token, "bot_chat_id": s.bot_chat_id}

@router.put("/mail", response_model=Dict)
def update_mail_settings(data: MailSettingsRequest):
    """Обновить настройки почты"""
    s = get_settings_db()
    if data.use_mail is not None:
        s.use_mail = data.use_mail
    if data.mail_host is not None:
        s.mail_host = data.mail_host
    if data.mail_port is not None:
        s.mail_port = data.mail_port
    if data.mail_login is not None:
        s.mail_login = data.mail_login
    if data.mail_password is not None:
        s.mail_password = data.mail_password
    s.save()
    return {"result": "updated"}

@router.put("/mail_notify", response_model=Dict)
def update_mail_notify_settings(data: MailNotifySettingsRequest):
    """Обновить настройки оповещений по почте"""
    mail_settings = load_mail_settings()
    for field, value in data.dict(exclude_unset=True).items():
        mail_settings[field] = value
    save_mail_settings(mail_settings)
    return {"result": "updated", "mail_notify": mail_settings}

@router.post("/bot/enable")
def enable_bot():
    """Включить бота (systemctl start openvpn-bot)"""
    try:
        subprocess.check_output("systemctl start openvpn-bot", shell=True)
        return {"result": "bot enabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bot/disable")
def disable_bot():
    """Отключить бота (systemctl stop openvpn-bot)"""
    try:
        subprocess.check_output("systemctl stop openvpn-bot", shell=True)
        return {"result": "bot disabled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bot/restart")
def restart_bot():
    """Перезапустить бота (systemctl restart openvpn-bot)"""
    try:
        subprocess.check_output("systemctl restart openvpn-bot", shell=True)
        return {"result": "bot restarted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))