from fastapi import FastAPI
from api.routers import keys, configs, sessions, statistics, settings, system
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="OpenVPN Management API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://127.0.0.1:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(keys.router, prefix="/keys", tags=["Keys"])
app.include_router(configs.router, prefix="/configs", tags=["Configs"])
app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
app.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])
app.include_router(system.router, prefix="/system", tags=["System"])