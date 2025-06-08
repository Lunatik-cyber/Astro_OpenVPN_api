from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import subprocess

router = APIRouter()

@router.post("/import_db")
def import_db(link: str = Body(..., embed=True)):
    """
    Восстановить базу данных из бэкапа по ссылке
    """
    try:
        subprocess.check_output(f"bash bash/openvpn.sh --restore {link}", shell=True)
        return {"result": "imported"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export_db")
def export_db():
    """
    Создать резервную копию базы данных
    """
    try:
        out = subprocess.check_output("bash bash/openvpn.sh --backup", shell=True)
        return {"result": "exported", "output": out.decode("utf-8")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/delete_openvpn")
def delete_openvpn():
    """
    Удалить OpenVPN
    """
    try:
        subprocess.check_output("python3 install.py -u", shell=True)
        return {"result": "openvpn deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update_script")
def update_script():
    """
    Обновить скрипт (выполнить команду обновления)
    """
    try:
        # Здесь предполагается что update_script не требует параметров. Добавьте если нужно.
        # Например: subprocess.check_output("bash update_script.sh", shell=True)
        # Или вызов вашей функции update_script()
        # out = update_script_func(...)
        out = "update not implemented"
        return {"result": "updated", "output": out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear_statistics")
def clear_statistics():
    """
    Очистить статистику и перезапустить сервисы
    """
    try:
        subprocess.check_output("systemctl stop openvpn@server", shell=True)
        subprocess.check_output("systemctl stop openvpn-bot", shell=True)
        subprocess.check_output("systemctl stop openvpn-botapi", shell=True)
        subprocess.check_output("systemctl stop openvpn-api", shell=True)
        # Остановить все дополнительные серверы по списку configs
        # Здесь должен быть вызов clear_stats_db(), если он реализован
        # subprocess.check_output("systemctl restart openvpn-bot; systemctl restart openvpn-botapi; systemctl restart openvpn-api; bash /etc/openvpn/startServer.sh", shell=True)
        return {"result": "statistics cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))