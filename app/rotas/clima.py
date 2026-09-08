import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.config import API_KEY, BASE_URL, GEO_URL
from app.utils import (
    CIDADES_MAP,
    gerar_variacoes,
    normalizar,
    sugerir_cidades,
)

router = APIRouter()


def _icone_clima(condicao: str) -> str:
    c = (condicao or "").lower()
    if any(x in c for x in ["clear", "limpo", "sol"]):
        return "☀️"
    if any(x in c for x in ["cloud", "nuvem"]):
        return "☁️"
    if any(x in c for x in ["rain", "chuva"]):
        return "🌧️"
    if any(x in c for x in ["thunder", "tempestade"]):
        return "⛈️"
    if any(x in c for x in ["snow", "neve"]):
        return "❄️"
    if any(x in c for x in ["mist", "fog", "névoa", "neblina"]):
        return "🌫️"
    return "🌡️"


def _geocodificar(nome_cidade: str) -> dict | None:
    params = {
        "q": nome_cidade,
        "limit": 1,
        "appid": API_KEY,
    }
    try:
        resposta = requests.get(GEO_URL, params=params, timeout=10)
    except requests.RequestException:
        return None
    if resposta.status_code != 200:
        return None
    resultados = resposta.json()
    if not resultados:
        return None
    return resultados[0]


def _consultar_weather_por_coords(lat: float, lon: float) -> dict | None:
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br",
    }
    try:
        resposta = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException:
        return None
    if resposta.status_code != 200:
        return None
    return resposta.json()


def _obter_nome_pt(geo_result: dict, norm: str) -> str:
    local_names = geo_result.get("local_names", {})
    nome_pt = local_names.get("pt")
    if nome_pt:
        return nome_pt
    if norm in CIDADES_MAP:
        return CIDADES_MAP[norm][1]
    return geo_result.get("name", "")


@router.get(
    "/clima",
    tags=["🌤️ Clima"],
    summary="Consultar clima por cidade",
    description=(
        "Retorna os dados climáticos em tempo real de uma cidade, "
        "consumindo a OpenWeather API. Inclui um resumo em texto legível "
        "e os dados estruturados em JSON.\n\n"
        "**Exemplo:** `/clima?cidade=São Paulo`\n\n"
        "A busca aceita variações: sem acentos, sem hifens, maiúsculas/minúsculas. "
        "O nome da cidade é sempre retornado em português "
        "(ex: \"Tokyo\" → \"Tóquio\", \"London\" → \"Londres\")."
    ),
    responses={
        200: {
            "description": "Dados climáticos retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "☀️ Dados climáticos para São Paulo",
                        "resumo": "☀️ Clima em São Paulo, BR:\n   • Condição: Céu limpo\n   • 🌡️ Temperatura: 28.5 °C (sensação térmica de 30.0 °C)\n   • 💧 Umidade: 60%\n   • 🌬️ Vento: 3.2 m/s\n   • ☁️ Nuvens: 0%",
                        "dados": {
                            "cidade": "São Paulo",
                            "pais": "BR",
                            "coordenadas": {"latitude": -23.55, "longitude": -46.63},
                            "clima": {"icone": "☀️", "condicao": "Clear", "descricao": "Céu limpo"},
                            "temperatura": {
                                "atual_c": 28.5,
                                "sensacao_termica_c": 30.0,
                                "minima_c": 25.0,
                                "maxima_c": 31.0,
                                "pressao_hpa": 1015,
                                "umidade_pct": 60,
                            },
                            "vento": {"velocidade_mps": 3.2, "direcao_graus": 150},
                            "nuvens_pct": 0,
                            "visibilidade_metros": 10000,
                            "horario_local": -10800,
                            "sol": {"nascer": 1700000000, "por": 1700040000},
                        },
                    }
                }
            },
        },
        404: {
            "description": "Cidade não encontrada. Pode incluir sugestões de cidades similares.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Cidade 'peltas' não encontrada.",
                        "sugestoes": ["Pelotas", "Petrópolis"],
                    }
                }
            },
        },
        500: {"description": "Chave da API OpenWeather ausente no `.env`."},
        503: {"description": "Erro de conexão com a OpenWeather."},
    },
)
def obter_clima(cidade: str = Query(..., description="Nome da cidade (ex: São Paulo, London, Tokyo, toquio)")):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="A chave da API do OpenWeather não foi encontrada no .env.",
        )

    norm = normalizar(cidade)

    if norm in CIDADES_MAP:
        query_inicial = CIDADES_MAP[norm][0]
    else:
        query_inicial = cidade

    variacoes = gerar_variacoes(query_inicial)

    geo_result = None
    erro_conexao = False
    for variacao in variacoes:
        resultado = _geocodificar(variacao)
        if resultado is not None:
            geo_result = resultado
            break
        try:
            requests.get(GEO_URL, params={"q": variacao, "limit": 1, "appid": API_KEY}, timeout=10)
        except requests.RequestException:
            erro_conexao = True

    if geo_result is None:
        if erro_conexao:
            raise HTTPException(
                status_code=503,
                detail="Erro ao conectar à OpenWeather.",
            )
        sugestoes = sugerir_cidades(norm)
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Cidade '{cidade}' não encontrada.",
                "sugestoes": sugestoes,
            },
        )

    lat = geo_result.get("lat")
    lon = geo_result.get("lon")
    nome_pt = _obter_nome_pt(geo_result, norm)
    pais = geo_result.get("country", "")

    dados = _consultar_weather_por_coords(lat, lon)

    if dados is None:
        raise HTTPException(
            status_code=503,
            detail="Erro ao obter dados climáticos da OpenWeather.",
        )

    condicao = dados.get("weather", [{}])[0].get("main", "")
    descricao = dados.get("weather", [{}])[0].get("description", "").capitalize()
    icone = _icone_clima(condicao)

    resumo = (
        f"{icone} Clima em {nome_pt}, {pais}:\n"
        f"   • Condição: {descricao}\n"
        f"   • 🌡️ Temperatura: {dados.get('main', {}).get('temp')} °C "
        f"(sensação térmica de {dados.get('main', {}).get('feels_like')} °C)\n"
        f"   • 💧 Umidade: {dados.get('main', {}).get('humidity')}%\n"
        f"   • 🌬️ Vento: {dados.get('wind', {}).get('speed')} m/s\n"
        f"   • ☁️ Nuvens: {dados.get('clouds', {}).get('all')}%"
    )

    clima_formatado = {
        "cidade": nome_pt,
        "pais": pais,
        "coordenadas": {
            "latitude": lat,
            "longitude": lon,
        },
        "clima": {
            "icone": icone,
            "condicao": condicao,
            "descricao": descricao,
        },
        "temperatura": {
            "atual_c": dados.get("main", {}).get("temp"),
            "sensacao_termica_c": dados.get("main", {}).get("feels_like"),
            "minima_c": dados.get("main", {}).get("temp_min"),
            "maxima_c": dados.get("main", {}).get("temp_max"),
            "pressao_hpa": dados.get("main", {}).get("pressure"),
            "umidade_pct": dados.get("main", {}).get("humidity"),
        },
        "vento": {
            "velocidade_mps": dados.get("wind", {}).get("speed"),
            "direcao_graus": dados.get("wind", {}).get("deg"),
        },
        "nuvens_pct": dados.get("clouds", {}).get("all"),
        "visibilidade_metros": dados.get("visibility"),
        "horario_local": dados.get("timezone"),
        "sol": {
            "nascer": dados.get("sys", {}).get("sunrise"),
            "por": dados.get("sys", {}).get("sunset"),
        },
    }

    return {
        "mensagem": f"{icone} Dados climáticos para {nome_pt}",
        "resumo": resumo,
        "dados": clima_formatado,
    }
