from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

tags_metadata = [
    {
        "name": "🏠 Início",
        "description": "Página inicial com apresentação e links rápidos da API.",
    },
    {
        "name": "🌤️ Clima",
        "description": "Consulta de dados climáticos em tempo real de qualquer cidade do mundo, "
        "consumindo a OpenWeather API.",
    },
]

app = FastAPI(
    title="☁️ API Clima",
    description=(
        "API que consome a **OpenWeather API** e retorna dados climáticos "
        "formatados de forma legível e amigável para humanos.\n\n"
        "### ✨ Recursos\n"
        "- 🔍 Consulta de clima por nome de cidade\n"
        "- 🌡️ Temperatura, sensação térmica, mínima e máxima\n"
        "- 💧 Umidade e pressão atmosférica\n"
        "- 🌬️ Vento (velocidade e direção)\n"
        "- ☁️ Cobertura de nuvens e visibilidade\n"
        "- 🌅 Horários de nascer e pôr do sol\n"
        "- 📝 Resumo em texto formatado\n\n"
        "### 🔗 Links úteis\n"
        "- [Documentação interativa](/docs)\n"
        "- [Especificação OpenAPI (JSON)](/openapi.json)\n"
        "- [Documentação ReDoc](/redoc)\n"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

from app.rotas import inicio, clima, docs  # noqa: E402

app.include_router(inicio.router)
app.include_router(clima.router)
app.include_router(docs.router)

_PNG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "PNGs")
app.mount("/pngs", StaticFiles(directory=_PNG_DIR), name="pngs")
