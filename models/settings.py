from pydantic import BaseModel
from typing import Optional

class SettingsBase(BaseModel):
    bot_token: str
    bot_chat_id: str
    telegraph_token: Optional[str]
    use_mail: bool
    mail_host: Optional[str]
    mail_port: Optional[int]
    mail_login: Optional[str]
    mail_password: Optional[str]
    subject: Optional[str] = "Пожалуйста, ваша VPN конфигурация"
    text: Optional[str] = "1 ключ - 1 устройство"

class SettingsOut(SettingsBase):
    class Config:
        orm_mode = True