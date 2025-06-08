from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConfigBase(BaseModel):
    port: int
    telnet_port: int
    address: str
    protocol: str
    subnet: str
    status: Optional[bool] = True

class ConfigCreate(ConfigBase):
    pass

class ConfigOut(ConfigBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True