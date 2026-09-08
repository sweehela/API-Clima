# ☁️ API Clima

> **by bobabi**

API que consome a [OpenWeather API](https://openweathermap.org/api) e retorna dados climáticos formatados de forma legível e amigável para humanos.

## ✨ Recursos

- 🔍 Consulta de clima por nome de cidade
- 🌡️ Temperatura, sensação térmica, mínima e máxima
- 💧 Umidade e pressão atmosférica
- 🌬️ Vento (velocidade e direção)
- ☁️ Cobertura de nuvens e visibilidade
- 🌅 Horários de nascer e pôr do sol
- 📝 Resumo em texto formatado
- 🌙/☀️ Interface interativa com tema claro/escuro
- 🔤 Busca flexível: aceita nomes sem acentos, sem hifens, maiúsculas/minúsculas
- 🌐 Nomes de cidades em português (ex: "Tokyo" → "Tóquio", "London" → "Londres")
- 💡 Sugestões de cidades similares quando o nome digitado não é encontrado (ex: "peltas" → Pelotas)

## 📁 Estrutura do projeto

```
api_clima/
├── app/
│   ├── __init__.py        # Instância do FastAPI e registro de rotas
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── utils.py           # Normalização de texto, mapeamento PT e sugestões
│   └── rotas/
│       ├── __init__.py
│       ├── inicio.py      # Rota "/" e "/redoc"
│       ├── clima.py       # Rota "/clima" (consulta à OpenWeather)
│       └── docs.py       # Rota "/docs" (interface interativa)
├── .env.example           # Exemplo de configuração de ambiente
├── .gitignore
├── main.py                # Ponto de entrada (executa o uvicorn)
├── README.md
└── requirements.txt       # Dependências do projeto
```

## 🚀 Como executar

1. **Pré-requisitos:** Python 3.10+

2. Clone o repositório e crie um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure sua chave da OpenWeather:
   - Copie `.env.example` para `.env`
   - Obtenha sua chave gratuitamente em [openweathermap.org/api](https://openweathermap.org/api)
   - Preencha o arquivo `.env`:

     ```
     OPENWEATHER_API_KEY=sua_chave_aqui
     ```

5. Inicie o servidor:

   ```bash
   python main.py
   ```

   ou

   ```bash
   python -m uvicorn app:app --reload
   ```

6. Acesse a interface interativa em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📡 Endpoints

### `GET /`

Página inicial com boas-vindas e link para a documentação interativa.

### `GET /clima`

Consulta os dados climáticos em tempo real de uma cidade.

| Parâmetro | Tipo   | Obrigatório | Descrição                              |
| --------- | ------ | ----------- | -------------------------------------- |
| `cidade`  | string | Sim         | Nome da cidade (ex: São Paulo, London) |

#### Busca flexível

A busca normaliza o nome da cidade antes de consultar a OpenWeather:

- **Sem acentos:** "toquio" funciona igual a "tóquio"
- **Sem hifens:** "nao me toque" funciona igual a "Não-Me-Toque"
- **Maiúsculas/minúsculas:** indiferente
- **Nome em português:** cidades com nomes diferentes em português são retornadas no idioma correto (ex: "Tokyo" → "Tóquio", "London" → "Londres", "Madrid" → "Madri")
- **Sugestões:** quando a cidade não é encontrada, a API retorna sugestões de cidades com nome similar (ex: "peltas" → sugere "Pelotas")

#### Resposta de sucesso (`200`)

```json
{
  "mensagem": "☀️ Dados climáticos para São Paulo",
  "resumo": "☀️ Clima em São Paulo, BR:\n   • Condição: Céu limpo\n   • 🌡️ Temperatura: 28.5 °C (sensação térmica de 30.0 °C)\n   • 💧 Umidade: 60%\n   • 🌬️ Vento: 3.2 m/s\n   • ☁️ Nuvens: 0%",
  "dados": {
    "cidade": "São Paulo",
    "pais": "BR",
    "coordenadas": { "latitude": -23.55, "longitude": -46.63 },
    "clima": { "icone": "☀️", "condicao": "Clear", "descricao": "Céu limpo" },
    "temperatura": {
      "atual_c": 28.5,
      "sensacao_termica_c": 30.0,
      "minima_c": 25.0,
      "maxima_c": 31.0,
      "pressao_hpa": 1015,
      "umidade_pct": 60
    },
    "vento": { "velocidade_mps": 3.2, "direcao_graus": 150 },
    "nuvens_pct": 0,
    "visibilidade_metros": 10000,
    "horario_local": -10800,
    "sol": { "nascer": 1700000000, "por": 1700040000 }
  }
}
```

#### Códigos de erro

| Status | Descrição                                       |
| ------ | ----------------------------------------------- |
| `404`  | Cidade não encontrada (inclui sugestões no corpo) |
| `500`  | Chave da API OpenWeather ausente no `.env`     |
| `503`  | Erro de conexão com a OpenWeather               |

##### Exemplo de erro 404 com sugestões

```json
{
  "detail": "Cidade 'peltas' não encontrada.",
  "sugestoes": ["Pelotas", "Palmas"]
}
```

### `GET /docs`

Interface interativa para consultar o clima de qualquer cidade de forma visual e polida, com suporte a tema claro/escuro.

### `GET /redoc`

Documentação técnica legível gerada automaticamente (ReDoc).

### `GET /openapi.json`

Especificação OpenAPI bruta em formato JSON.

## 🛠️ Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/) — framework web
- [Uvicorn](https://www.uvicorn.org/) — servidor ASGI
- [OpenWeather API](https://openweathermap.org/api) — fonte dos dados climáticos
- [ReDoc](https://redocly.com/redoc/) — documentação técnica
