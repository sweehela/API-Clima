import requests
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.config import API_KEY, BASE_URL, GEO_URL, IBGE_URL
from app.utils import (
    CIDADES_MAP,
    gerar_variacoes,
    normalizar,
    sigla_estado,
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


def _geocodificar_todos(nome_cidade: str, limite: int = 5) -> tuple[list, bool]:
    """Consulta a API de geocodificação e retorna (resultados, erro_conexao).

    Retorna *todos* os resultados encontrados (até `limite`), para que a
    chamadora possa desambiguar cidades de mesmo nome.
    """
    params = {
        "q": nome_cidade,
        "limit": limite,
        "appid": API_KEY,
    }
    try:
        resposta = requests.get(GEO_URL, params=params, timeout=10)
    except requests.RequestException:
        return [], True
    if resposta.status_code != 200:
        return [], False
    return resposta.json(), False


def _validar_municipios_br(nome_cidade: str) -> set[tuple[str, str]] | None:
    """Consulta a API do IBGE e retorna um conjunto de (nome_normalizado, sigla_uf)
    para os municípios brasileiros cujo nome corresponde a `nome_cidade`.

    Retorna None quando a API do IBGE está indisponível (nesse caso, a
    chamadora deve preservar os resultados da geocodificação sem filtrar).
    """
    try:
        resposta = requests.get(
            IBGE_URL,
            params={"nome": nome_cidade, "limit": 50},
            timeout=10,
        )
    except requests.RequestException:
        return None
    if resposta.status_code != 200:
        return None
    dados = resposta.json()
    norm_alvo = normalizar(nome_cidade)
    validos = set()
    for mun in dados:
        nome = mun.get("nome", "")
        if normalizar(nome) == norm_alvo:
            uf = mun.get("microrregiao", {}).get("mesorregiao", {}).get("UF", {})
            sigla = uf.get("sigla", "")
            if sigla:
                validos.add((norm_alvo, sigla))
    return validos


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
        "(ex: \"Tokyo\" → \"Tóquio\", \"London\" → \"Londres\").\n\n"
        "Quando existem várias cidades com o mesmo nome (ex: \"Bom Jesus\"), "
        "a API retorna uma lista de opções (com país e estado) para o usuário "
        "selecionar. Informe o parâmetro `estado` para escolher uma específica "
        "(ex: `/clima?cidade=Bom Jesus&estado=RS`)."
    ),
    responses={
        200: {
            "description": "Dados climáticos retornados com sucesso, ou lista de cidades para desambiguação.",
            "content": {
                "application/json": {
                    "examples": {
                        "clima": {
                            "summary": "Clima de uma cidade",
                            "value": {
                                "mensagem": "☀️ Dados climáticos para Pelotas",
                                "resumo": "☀️ Clima em Pelotas, BR - RS:\n   • Condição: Céu limpo\n   • 🌡️ Temperatura: 28.5 °C (sensação térmica de 30.0 °C)\n   • 💧 Umidade: 60%\n   • 🌬️ Vento: 3.2 m/s\n   • ☁️ Nuvens: 0%",
                                "dados": {
                                    "cidade": "Pelotas",
                                    "pais": "BR",
                                    "estado": "RS",
                                    "coordenadas": {"latitude": -31.77, "longitude": -52.34},
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
                            },
                        },
                        "desambiguacao": {
                            "summary": "Várias cidades com o mesmo nome",
                            "value": {
                                "acao": "selecionar",
                                "mensagem": "🔍 Foram encontradas 5 cidades chamadas 'Bom Jesus'. Selecione a desejada:",
                                "cidades": [
                                    {"nome": "Bom Jesus", "pais": "BR", "estado": "RS", "estado_nome": "Rio Grande do Sul", "latitude": -28.67, "longitude": -50.43},
                                    {"nome": "Bom Jesus", "pais": "BR", "estado": "PI", "estado_nome": "Piauí", "latitude": -9.07, "longitude": -44.36},
                                ],
                            },
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
def obter_clima(
    cidade: str = Query(..., description="Nome da cidade (ex: São Paulo, London, Tokyo, toquio)"),
    estado: str = Query(None, description="Sigla ou nome do estado para desambiguar cidades de mesmo nome (ex: RS, Rio Grande do Sul)"),
):
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

    resultados_geo = []
    erro_conexao = False
    for variacao in variacoes:
        resultados, erro = _geocodificar_todos(variacao)
        if erro:
            erro_conexao = True
        if resultados:
            resultados_geo = resultados
            break

    if not resultados_geo:
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

    # Mantém apenas resultados cujo nome bate com a cidade pesquisada
    # (a API de geocodificação às vezes inclui localidades próximas).
    norm_query = normalizar(query_inicial)
    candidatos = [
        r for r in resultados_geo
        if normalizar(r.get("name", "")) == norm_query
    ]
    if not candidatos:
        candidatos = resultados_geo

    # Valida municípios brasileiros contra a API do IBGE, removendo
    # localidades que não são municípios reais (a geocodificação do
    # OpenWeather pode retornar falsos positivos com o mesmo nome).
    candidatos_br = [r for r in candidatos if r.get("country") == "BR"]
    if candidatos_br:
        municipios_validos = _validar_municipios_br(query_inicial)
        if municipios_validos is not None:
            validos_filtrados = []
            for r in candidatos_br:
                sigla = sigla_estado(r)
                if (norm_query, sigla) in municipios_validos:
                    validos_filtrados.append(r)
            if validos_filtrados:
                candidatos = validos_filtrados + [
                    r for r in candidatos if r.get("country") != "BR"
                ]

    # Remove duplicatas (mesma cidade, país e estado) — a geocodificação
    # pode retornar o mesmo local com coordenadas levemente diferentes.
    vistos = set()
    unicos = []
    for r in candidatos:
        chave = (normalizar(r.get("name", "")), r.get("country", ""), sigla_estado(r))
        if chave not in vistos:
            vistos.add(chave)
            unicos.append(r)
    candidatos = unicos

    # Filtra por estado, quando informado
    if estado:
        norm_estado = normalizar(estado)
        filtrados = []
        for r in candidatos:
            sigla = sigla_estado(r)
            nome_estado = (r.get("state") or "").strip()
            if norm_estado == normalizar(sigla) or norm_estado == normalizar(nome_estado):
                filtrados.append(r)
        if filtrados:
            candidatos = filtrados

    # Desambiguação: várias cidades com o mesmo nome
    if len(candidatos) > 1:
        opcoes = []
        for r in candidatos:
            opcoes.append({
                "nome": _obter_nome_pt(r, norm),
                "pais": r.get("country", ""),
                "estado": sigla_estado(r),
                "estado_nome": (r.get("state") or "").strip(),
                "latitude": r.get("lat"),
                "longitude": r.get("lon"),
            })
        return {
            "acao": "selecionar",
            "mensagem": (
                f"🔍 Foram encontradas {len(opcoes)} cidades chamadas "
                f"'{cidade}'. Selecione a desejada:"
            ),
            "cidades": opcoes,
        }

    geo_result = candidatos[0]
    lat = geo_result.get("lat")
    lon = geo_result.get("lon")
    nome_pt = _obter_nome_pt(geo_result, norm)
    pais = geo_result.get("country", "")
    sigla = sigla_estado(geo_result)

    dados = _consultar_weather_por_coords(lat, lon)

    if dados is None:
        raise HTTPException(
            status_code=503,
            detail="Erro ao obter dados climáticos da OpenWeather.",
        )

    condicao = dados.get("weather", [{}])[0].get("main", "")
    descricao = dados.get("weather", [{}])[0].get("description", "").capitalize()
    icone = _icone_clima(condicao)

    local = f"{pais} - {sigla}" if sigla else pais

    resumo = (
        f"{icone} Clima em {nome_pt}, {local}:\n"
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
        "estado": sigla,
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
