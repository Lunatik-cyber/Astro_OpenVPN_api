from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class ConfigInfo(BaseModel):
    config: Union[int, str]
    port: Optional[Union[int, str]]
    protocol: Optional[str]

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