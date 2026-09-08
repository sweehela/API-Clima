import unicodedata


def remover_acentos(texto: str) -> str:
    normalized = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def normalizar(texto: str) -> str:
    sem_acentos = remover_acentos(texto)
    sem_hifens = sem_acentos.replace("-", " ")
    return " ".join(sem_hifens.lower().split())


def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


CIDADES_MAP = {
    "toquio": ("Tokyo", "Tóquio"),
    "tokyo": ("Tokyo", "Tóquio"),
    "nova york": ("New York", "Nova York"),
    "new york": ("New York", "Nova York"),
    "londres": ("London", "Londres"),
    "london": ("London", "Londres"),
    "pequim": ("Beijing", "Pequim"),
    "beijing": ("Beijing", "Pequim"),
    "moscou": ("Moscow", "Moscou"),
    "moscow": ("Moscow", "Moscou"),
    "madri": ("Madrid", "Madri"),
    "madrid": ("Madrid", "Madri"),
    "roma": ("Rome", "Roma"),
    "rome": ("Rome", "Roma"),
    "berlim": ("Berlin", "Berlim"),
    "berlin": ("Berlin", "Berlim"),
    "viena": ("Vienna", "Viena"),
    "vienna": ("Vienna", "Viena"),
    "montevideu": ("Montevideo", "Montevidéu"),
    "montevideo": ("Montevideo", "Montevidéu"),
    "assuncao": ("Asuncion", "Assunção"),
    "asuncion": ("Asuncion", "Assunção"),
    "atenas": ("Athens", "Atenas"),
    "athens": ("Athens", "Atenas"),
    "estocolmo": ("Stockholm", "Estocolmo"),
    "stockholm": ("Stockholm", "Estocolmo"),
    "varsavia": ("Warsaw", "Varsóvia"),
    "warsaw": ("Warsaw", "Varsóvia"),
    "genebra": ("Geneva", "Genebra"),
    "geneva": ("Geneva", "Genebra"),
    "milao": ("Milan", "Milão"),
    "milano": ("Milan", "Milão"),
    "milan": ("Milan", "Milão"),
    "florenca": ("Florence", "Florença"),
    "florence": ("Florence", "Florença"),
    "veneza": ("Venice", "Veneza"),
    "venice": ("Venice", "Veneza"),
    "seul": ("Seoul", "Seul"),
    "seoul": ("Seoul", "Seul"),
    "bangcoc": ("Bangkok", "Bangcoc"),
    "bangkok": ("Bangkok", "Bangcoc"),
    "jacarta": ("Jakarta", "Jacarta"),
    "jakarta": ("Jakarta", "Jacarta"),
    "nova deli": ("New Delhi", "Nova Déli"),
    "new delhi": ("New Delhi", "Nova Déli"),
    "deli": ("Delhi", "Déli"),
    "delhi": ("Delhi", "Déli"),
    "cairo": ("Cairo", "Cairo"),
    "havana": ("Havana", "Havana"),
    "haia": ("The Hague", "Haia"),
    "the hague": ("The Hague", "Haia"),
    "cidade do mexico": ("Mexico City", "Cidade do México"),
    "mexico city": ("Mexico City", "Cidade do México"),
    "munique": ("Munich", "Munique"),
    "munich": ("Munich", "Munique"),
    "colonia": ("Cologne", "Colônia"),
    "cologne": ("Cologne", "Colônia"),
    "nao me toque": ("Não-Me-Toque", "Não-Me-Toque"),
}

CIDADES_CONHECIDAS = [
    "Porto Alegre", "Florianópolis", "Curitiba", "São Paulo", "Rio de Janeiro",
    "Belo Horizonte", "Vitória", "Salvador", "Brasília", "Goiânia", "Cuiabá",
    "Campo Grande", "Palmas", "Manaus", "Rio Branco", "Porto Velho", "Boa Vista",
    "Macapá", "Belém", "São Luís", "Teresina", "Fortaleza", "Natal", "João Pessoa",
    "Recife", "Maceió", "Aracaju",
    "Pelotas", "Não-Me-Toque", "Londrina", "Maringá", "Campinas", "Santos",
    "Niterói", "Uberlândia", "Juiz de Fora", "Petrópolis", "Caxias do Sul",
    "Santa Maria", "Passo Fundo", "Bagé", "Uruguaiana", "Ijuí", "Erechim",
    "Santana do Livramento", "Cachoeira do Sul", "São Gabriel", "Alegrete",
    "São Borja", "Santiago", "Novo Hamburgo", "São Leopoldo", "Canoas",
    "Gravataí", "Viamão", "Alvorada", "Sapucaia do Sul", "Cachoeirinha",
    "Osório", "Três Passos", "Carazinho", "Soledade", "Cruz Alta",
    "Santo Ângelo", "Santa Rosa", "Bento Gonçalves", "Gramado", "Canela",
    "Torres", "Capão da Canoa", "Tramandaí", "Joinville", "Blumenau",
    "Chapecó", "Lages", "Criciúma", "Tubarão",
    "Tóquio", "Londres", "Paris", "Madri", "Roma", "Berlim", "Viena", "Moscou",
    "Pequim", "Nova York", "Los Angeles", "Buenos Aires", "Montevidéu",
    "Assunção", "Santiago", "Lima", "Bogotá", "Caracas", "Havana",
    "Cidade do México", "Washington", "Ottawa", "Toronto", "Seul", "Bangcoc",
    "Jacarta", "Manila", "Nova Déli", "Cairo", "Atenas", "Estocolmo",
    "Varsóvia", "Genebra", "Milão", "Florença", "Veneza", "Haia",
    "Munique", "Colônia", "Estugarda", "Frankfurt", "Hamburgo",
]


def gerar_variacoes(nome: str) -> list:
    variacoes = [nome]
    sem_hifens = nome.replace("-", " ")
    if sem_hifens != nome:
        variacoes.append(sem_hifens)
    sem_acentos = remover_acentos(nome)
    if sem_acentos != nome:
        variacoes.append(sem_acentos)
    sem_acentos_hifens = sem_acentos.replace("-", " ")
    if sem_acentos_hifens not in variacoes:
        variacoes.append(sem_acentos_hifens)
    norm = normalizar(nome)
    if norm not in [v.lower() for v in variacoes]:
        variacoes.append(norm)
    if nome.lower() not in [v.lower() for v in variacoes]:
        variacoes.append(nome.lower())
    return variacoes


def sugerir_cidades(nome_normalizado: str, limite: int = 5) -> list:
    distancias = []
    for cidade in CIDADES_CONHECIDAS:
        norm_cidade = normalizar(cidade)
        dist = levenshtein(nome_normalizado, norm_cidade)
        distancias.append((dist, cidade))
    distancias.sort(key=lambda x: x[0])
    limite_dist = max(2, len(nome_normalizado) // 3)
    sugestoes = [c for d, c in distancias if d <= limite_dist][:limite]
    return sugestoes
