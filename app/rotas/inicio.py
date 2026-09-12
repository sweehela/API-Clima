from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["🏠 Início"],
    summary="Página inicial",
    description="Página de boas-vindas com um resumo da API e link para a documentação interativa.",
)
def home():
    return """
    <html>
      <head><meta charset="utf-8"><title>API Clima</title></head>
      <body style="font-family:Segoe UI,Arial;max-width:700px;margin:40px auto;line-height:1.6;background:#0f172a;color:#e2e8f0;text-align:center">
        <img src="/pngs/apiClimaLogo.png" alt="API Clima" style="max-width:180px;width:100%;height:auto;margin:0 auto 6px;display:block">
        <p style="font-style:italic;color:#94a3b8;font-size:.85rem;margin-top:0">by bobabi</p>
        <p>Bem-vindo(a)! Use o endpoint abaixo para consultar o clima de qualquer cidade.</p>
        <p>➡️ <code style="background:#1e293b;padding:4px 8px;border-radius:6px">GET /clima?cidade=NOME_DA_CIDADE</code></p>
        <p>📄 Documentação interativa: <a style="color:#38bdf8" href="/docs">/docs</a></p>
      </body>
    </html>
    """


@router.get("/redoc", include_in_schema=False, tags=["🏠 Início"])
def redoc_html():
    from fastapi.openapi.docs import get_redoc_html
    from app import app
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="☁️ API Clima · ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.5/bundles/redoc.standalone.js",
        with_google_fonts=False,
    )
