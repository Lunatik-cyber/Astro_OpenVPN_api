<p align="center">
  <img src="logo.svg" width="180" alt="OpenVPN API Logo"/>
</p>

<h1 align="center">OpenVPN Management API</h1>
<p align="center">
  <b>REST API для автоматизации и управления вашим OpenVPN-сервером</b>
</p>
<p align="center">
  <img alt="Ubuntu 20.04+" src="https://img.shields.io/badge/Ubuntu-20.04%2B-orange?logo=ubuntu">
  <img alt="Python 3.8+" src="https://img.shields.io/badge/Python-3.8+-blue?logo=python">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-✓-green?logo=fastapi">
</p>

---

## 🚀 Возможности

- **Управление ключами:** создание, удаление, блокировка, рассылка, перенос, массовые действия.
- **Управление конфигами:** добавление, удаление, активация/деактивация, просмотр связанных ключей.
- **История сессий** и детальная статистика по серверу.
- **Настройки:** интеграция с Telegram-ботом, email-уведомления.
- **Системные операции:** резервное копирование, импорт/экспорт БД, обновление, очистка статистики.
- **Всё через REST API и JSON**.  
- **Swagger/OpenAPI:** docs по адресу `/docs`.

---

## 📦 Требования

- **Ubuntu 20.04+** (**обязательно!**)
- Python **3.8+**
- Установленный и рабочий OpenVPN
- Bash-скрипты (`openvpn.sh`, `install.py` и др.) в нужных путях
- Доступ к SMTP (если используете email-уведомления)

---

## 🐍 Используемые библиотеки

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pydantic](https://docs.pydantic.dev/) (валидация данных)
- [python-multipart](https://andrew-d.github.io/python-multipart/) (для upload)

Установка всех зависимостей:
```bash
pip install -r requirements.txt
```

---

## ⚡️ Установка

```bash
# Клонируйте репозиторий
cd /lib/openvpn
git clone https://github.com/Lunatik-cyber/Astro_OpenVPN_api.git

# Переименовываем папку
mv Astro_OpenVPN_api api

# Установите зависимости
cd /lib/openvpn/api
pip install -r requirements.txt

# Запустите API
IP=$(ip -4 addr | sed -ne 's|^.* inet \([^/]*\)/.* scope global.*$|\1|p' | head -1)
uvicorn api.app:app --reload --host $IP --port 8666
```

- **Swagger-документация:** [http://localhost:8666/docs](http://localhost:8666/docs)
- **Redoc:** [http://localhost:8666/redoc](http://localhost:8666/redoc)

---

## 🗄️ Структура таблиц (ORM)

### Key (Ключ)

| Поле         | Тип           | Описание                        |
|--------------|---------------|---------------------------------|
| id           | Integer (PK)  | Уникальный идентификатор        |
| name         | String        | Имя ключа                       |
| email        | String        | Email пользователя              |
| days         | Integer       | Срок действия (дней)            |
| config_id    | Integer (FK)  | Привязка к конфигу              |
| status       | Boolean       | Активен/блокирован              |
| connected    | Boolean       | Сейчас подключён                |
| expired      | DateTime      | Дата истечения                  |
| used_total   | Integer       | Сколько раз использовался       |
| free_key     | Boolean       | Свободный ключ                  |
| created      | DateTime      | Дата создания                   |
| updated      | DateTime      | Дата обновления                 |

### Config (Конфиг)

| Поле        | Тип           | Описание                      |
|-------------|---------------|-------------------------------|
| id          | Integer (PK)  | Уникальный идентификатор      |
| port        | Integer       | Порт                          |
| telnet_port | Integer       | Telnet-порт                   |
| address     | String        | IP/домен                      |
| protocol    | String        | udp/tcp                       |
| subnet      | String        | VPN-подсеть                   |
| status      | Boolean       | Активен/нет                   |
| created     | DateTime      | Дата создания                 |
| updated     | DateTime      | Дата обновления               |

### Session (Сессии)

| Поле                | Тип           | Описание                      |
|---------------------|---------------|-------------------------------|
| id                  | Integer (PK)  | Уникальный идентификатор      |
| key_id              | Integer (FK)  | Ключ                          |
| ip                  | String        | IP                            |
| connected           | DateTime      | Время подключения             |
| disconnected        | DateTime      | Время отключения              |
| total_bytes         | BigInt        | Трафик                        |
| total_connected_time| Integer       | Время в сети (сек)            |

### Settings (Настройки)

| Поле           | Тип      | Описание                   |
|----------------|----------|----------------------------|
| id             | Integer  | PK                         |
| bot_token      | String   | Telegram Bot Token         |
| bot_chat_id    | String   | Telegram Chat ID           |
| telegraph_token| String   | Telegraph Token            |
| use_mail       | Boolean  | Использовать email         |
| mail_host      | String   | SMTP сервер                |
| mail_port      | Integer  | SMTP порт                  |
| mail_login     | String   | SMTP логин                 |
| mail_password  | String   | SMTP пароль                |

---

## 🎨 Логотип

<p align="center">
  <img src="logo.svg" width="200" alt="OpenVPN API Logo"/><br>
  <i><b>OpenVPN API: Automation Gateway</b></i>
</p>

---

## 📚 Примеры запросов и ответов

### Получить список всех ключей

**GET** `/keys?by=all`

**Пример ответа:**
```json
[
  {
    "id": 1,
    "name": "user1",
    "email": "user1@example.com",
    "days": 30,
    "config_id": 1,
    "status": true,
    "connected": false,
    "expired": "2025-07-08T00:00:00"
  }
]
```

---

### Создать ключ

**POST** `/keys`

**Тело запроса:**
```json
{
  "name": "user1",
  "days": 30,
  "amount": 1,
  "config_id": 1,
  "email": "user1@example.com"
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "user1",
  ...
}
```

---

### Массовая блокировка ключей

**POST** `/keys/bulk/block`

**Тело запроса:**
```json
{"ids": [1,2,3]}
```
**Ответ:**
```json
{"result": "blocked_bulk"}
```

---

### Получить статистику

**GET** `/statistics`

**Ответ:**
```json
{
  "total_keys": 42,
  "active_keys": 30,
  "blocked_keys": 2,
  "connected_keys": 8,
  "expired_keys": 3,
  "total_configs": 2,
  "total_traffic": "18.7 GB",
  "configs": [
    {
      "id": 1,
      "port": 1194,
      "protocol": "udp",
      "address": "vpn.example.com"
    }
  ]
}
```

---

### Получить настройки

**GET** `/settings`

**Ответ:**
```json
{
  "bot_token": "12345:...",
  "bot_chat_id": "-123456789",
  "use_mail": true,
  "mail_host": "smtp.example.com",
  "mail_port": 465,
  "mail_login": "vpn@example.com"
}
```

---

## 📝 Основные эндпоинты

| HTTP      | URL                           | Тело запроса / Query           | Описание                           |
|-----------|-------------------------------|-------------------------------|------------------------------------|
| GET       | `/keys`                       | by, value                     | Получить список ключей с фильтрами |
| POST      | `/keys`                       | name, days, amount, config_id | Создать ключ                      |
| DELETE    | `/keys/{id}`                  | -                             | Удалить ключ                      |
| PUT       | `/keys/{id}`                  | days, email                   | Изменить срок/email ключа          |
| POST      | `/keys/{id}/block`            | -                             | Заблокировать ключ                |
| POST      | `/keys/bulk/block`            | ids: [int]                    | Массовая блокировка ключей         |
| ...       | ...                           | ...                           | ... (см. Swagger документацию)     |

Больше примеров — в `/docs`!

---

## 💡 Рекомендации

- **API требует защищенного окружения!**  
  Размещайте только за Firewall/VPN, добавьте авторизацию.
- **Рекомендуется запускать на свежей Ubuntu 20.04+ и Python 3.8+**
- Для production — отключайте `--reload` и запускайте через systemd/gunicorn.

---

## 🪪 Лицензия

[MIT License](LICENSE)