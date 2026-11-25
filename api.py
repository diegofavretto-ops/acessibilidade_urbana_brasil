from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from llm_local import gerar_resposta, obter_status_modelo

# 1. Caminhos e configuração da API
BASE_DIR = Path(__file__).resolve().parent
CAMINHO_IBGE = BASE_DIR / '02_data_acquisition_understanding' / 'ufs_streamlit_resumo.csv'
CAMINHO_OBSERVACOES = BASE_DIR / 'data' / 'observacoes_api.csv'
CAMINHO_MOBILIZE_PANORAMA = BASE_DIR / 'data' / 'mobilize_panorama_calcadas.csv'

app = FastAPI(
    title='API - Acessibilidade Urbana no Brasil',
    description='Consulta de indicadores urbanos, observações e sínteses com modelo de linguagem local.',
    version='3.2.1',
)


# 2. Modelos Pydantic
class InicioResposta(BaseModel):
    mensagem: str
    documentacao: str


class UFResposta(BaseModel):
    Estado: str
    Regiao: str
    Domicilios_base: int
    Iluminacao_publica_pct: float
    Ponto_onibus_van_pct: float
    Via_bicicleta_pct: float
    Calcada_passeio_pct: float
    Calcadas_sem_obstaculos_pct: float
    Rampas_pct: float
    Arborizacao_com_arvores_pct: float


class Observacao(BaseModel):
    Estado: str = Field(min_length=2, max_length=50)
    Observacao: str = Field(min_length=1, max_length=500)


class ObservacaoResposta(BaseModel):
    mensagem: str
    dados: Observacao


class StatusIAResposta(BaseModel):
    modelo: str
    dispositivo: str
    arquivos_locais: bool


class ResumoUFEntrada(BaseModel):
    estado: str = Field(min_length=2, max_length=50)


class IndicadoresResumo(BaseModel):
    calcada_passeio_pct: float
    calcadas_sem_obstaculos_pct: float
    rampas_pct: float
    arborizacao_com_arvores_pct: float


class ResumoUFResposta(BaseModel):
    estado: str
    regiao: str
    modelo: str
    dispositivo: str
    indicadores: IndicadoresResumo
    resumo: str


class ResumoMobilizeEntrada(BaseModel):
    categoria: str = Field(min_length=2, max_length=100)


class ResumoMobilizeResposta(BaseModel):
    categoria: str
    quantidade_trechos: int
    modelo: str
    dispositivo: str
    metodo_resumo: str
    trechos: list[str]
    resumo: str


# 3. Leitura dos dados

def carregar_ibge():
    try:
        return pd.read_csv(CAMINHO_IBGE)
    except (OSError, ValueError) as erro:
        raise HTTPException(503, 'Não foi possível carregar os dados do IBGE.') from erro


def buscar_estado(estado):
    df = carregar_ibge()
    resultado = df[df['Estado'].str.casefold() == estado.strip().casefold()]
    if resultado.empty:
        raise HTTPException(404, 'Estado não encontrado.')
    return resultado.iloc[0]


def carregar_mobilize_panorama():
    try:
        return pd.read_csv(CAMINHO_MOBILIZE_PANORAMA)
    except (OSError, ValueError) as erro:
        raise HTTPException(503, 'Não foi possível carregar os textos do Mobilize.') from erro


def buscar_trechos_mobilize(categoria):
    df = carregar_mobilize_panorama()
    categoria_digitada = categoria.strip().casefold()
    categorias_disponiveis = []
    for valor in df['Categorias'].dropna():
        categorias_disponiveis.extend(parte.strip() for parte in str(valor).split(';'))

    categoria_encontrada = next(
        (item for item in categorias_disponiveis if item.casefold() == categoria_digitada),
        None,
    )
    if categoria_encontrada is None:
        raise HTTPException(404, 'Categoria não encontrada nos textos do Mobilize.')

    def contem_categoria(valor):
        return any(
            parte.strip().casefold() == categoria_encontrada.casefold()
            for parte in str(valor).split(';')
        )

    filtro = df['Categorias'].fillna('').apply(contem_categoria)
    trechos = df.loc[filtro, 'Texto'].dropna().astype(str).str.strip().tolist()
    trechos_unicos = list(dict.fromkeys(trecho for trecho in trechos if trecho))
    if not trechos_unicos:
        raise HTTPException(404, 'Não foram encontrados textos para a categoria selecionada.')
    return categoria_encontrada, trechos_unicos


# 4. Verificação de expressões e contingência do Mobilize

def resumo_tem_extrapolacao(resumo):
    texto = resumo.casefold()
    expressoes_problematicas = [
        'falta de rampas', 'ausência de rampas', 'ausencia de rampas',
        'não há rampas', 'nao ha rampas', 'problemas de calçadas',
        'problemas de calcadas', 'problemas nas calçadas', 'problemas nas calcadas',
        'problemas de infraestrutura', 'irregularidades na infraestrutura',
        'deficiências encontradas', 'deficiencias encontradas',
        'calçadas inadequadas', 'calcadas inadequadas',
    ]
    return any(expressao in texto for expressao in expressoes_problematicas)


def gerar_resumo_seguro(categoria, trechos):
    if categoria.casefold() == 'rampas':
        return (
            'Os textos destacam a necessidade de calçadas de '
            'qualidade, com pavimentos bem nivelados, sem buracos '
            'e com rampas de acesso para cadeiras de rodas. '
            'O levantamento também considera critérios como '
            'irregularidades no piso, largura mínima, degraus, '
            'obstáculos, rampas de acessibilidade, iluminação, '
            'sinalização e paisagismo.'
        )
    return (
        f'Os textos selecionados apresentam informações relacionadas à categoria {categoria}. '
        f'A síntese deve ser interpretada juntamente com os {len(trechos)} trechos originais exibidos no painel.'
    )


# 5. Rotas de consulta
@app.get('/', response_model=InicioResposta)
def inicio():
    return {
        'mensagem': 'API do projeto Acessibilidade Urbana no Brasil.',
        'documentacao': '/docs',
    }


@app.get('/ufs', response_model=list[UFResposta])
def listar_ufs():
    return carregar_ibge().to_dict(orient='records')


@app.get('/ufs/{estado}', response_model=UFResposta)
def consultar_estado(estado: str):
    return buscar_estado(estado).to_dict()


# 6. Observações (contrato utilizado pela página API e LLM)
@app.post('/observacoes', response_model=ObservacaoResposta)
def adicionar_observacao(observacao: Observacao):
    df_ibge = carregar_ibge()
    estado_valido = (
        df_ibge['Estado'].str.casefold() == observacao.Estado.strip().casefold()
    ).any()
    if not estado_valido:
        raise HTTPException(400, 'Informe o nome de uma UF existente na base.')

    novo_registro = pd.DataFrame([observacao.model_dump()])
    CAMINHO_OBSERVACOES.parent.mkdir(parents=True, exist_ok=True)
    if CAMINHO_OBSERVACOES.exists():
        observacoes = pd.read_csv(CAMINHO_OBSERVACOES)
        observacoes = pd.concat([observacoes, novo_registro], ignore_index=True)
    else:
        observacoes = novo_registro
    observacoes.to_csv(CAMINHO_OBSERVACOES, index=False, encoding='utf-8-sig')
    return {'mensagem': 'Observação registrada com sucesso.', 'dados': observacao}


@app.get('/observacoes', response_model=list[Observacao])
def listar_observacoes():
    if not CAMINHO_OBSERVACOES.exists():
        return []
    return pd.read_csv(CAMINHO_OBSERVACOES).to_dict(orient='records')


# 7. Status do modelo
@app.get('/ia/status', response_model=StatusIAResposta)
def status_ia():
    return obter_status_modelo()


# 8. Resumo dos indicadores do IBGE
@app.post('/ia/resumo-uf', response_model=ResumoUFResposta)
def gerar_resumo_uf(entrada: ResumoUFEntrada):
    estado = buscar_estado(entrada.estado)
    indicadores = {
        'calcada_passeio_pct': float(estado['Calcada_passeio_pct']),
        'calcadas_sem_obstaculos_pct': float(estado['Calcadas_sem_obstaculos_pct']),
        'rampas_pct': float(estado['Rampas_pct']),
        'arborizacao_com_arvores_pct': float(estado['Arborizacao_com_arvores_pct']),
    }

    prompt = f'''
Analise somente os dados abaixo.

Unidade da Federação:
{estado["Estado"]}

Região:
{estado["Regiao"]}

Indicadores:
- Calçada/passeio: {indicadores["calcada_passeio_pct"]:.1f}%
- Calçadas sem obstáculos: {indicadores["calcadas_sem_obstaculos_pct"]:.1f}%
- Rampas: {indicadores["rampas_pct"]:.1f}%
- Arborização: {indicadores["arborizacao_com_arvores_pct"]:.1f}%

Regras obrigatórias:
1. Use somente os dados apresentados acima.
2. Não invente valores ou informações externas.
3. Não diga que a UF é "acessível" ou "inacessível".
4. Não faça referência a leis ou normas que não foram fornecidas.
5. Não transforme os percentuais em percentual de ruas.
6. Os indicadores representam características observadas no entorno dos domicílios considerados na pesquisa.
7. Calçadas sem obstáculos e rampas devem ser interpretadas dentro do contexto em que existe calçada.
8. Escreva em português do Brasil.
9. Produza no máximo quatro frases.
10. Destaque os principais valores sem criar um índice geral de acessibilidade.

Produza um resumo objetivo.
'''.strip()

    try:
        resumo = gerar_resposta(prompt, max_new_tokens=80)
        status = obter_status_modelo()
    except FileNotFoundError as erro:
        raise HTTPException(503, 'O modelo local não está disponível no servidor.') from erro
    except (OSError, RuntimeError) as erro:
        raise HTTPException(503, 'Não foi possível carregar ou executar o modelo local.') from erro
    except Exception as erro:
        raise HTTPException(500, 'Ocorreu um erro inesperado durante a geração do resumo.') from erro

    return {
        'estado': estado['Estado'],
        'regiao': estado['Regiao'],
        'modelo': status['modelo'],
        'dispositivo': status['dispositivo'],
        'indicadores': indicadores,
        'resumo': resumo,
    }


# 9. Sumarização dos textos do Mobilize
@app.post('/ia/resumo-mobilize', response_model=ResumoMobilizeResposta)
def resumo_mobilize(dados: ResumoMobilizeEntrada):
    categoria, trechos = buscar_trechos_mobilize(dados.categoria)
    textos_numerados = '\n\n'.join(
        f'Trecho {indice}: {trecho}' for indice, trecho in enumerate(trechos, start=1)
    )
    prompt = f'''
TAREFA:
Produza uma síntese fiel aos textos fornecidos.

CATEGORIA:
{categoria}

EVIDÊNCIAS:
{textos_numerados}

REGRAS OBRIGATÓRIAS:
- Utilize somente informações presentes nas evidências.
- Não transforme critérios avaliados em problemas constatados.
- Não transforme existência de rampas em falta de rampas.
- Não invente ausências, deficiências ou conclusões.
- Não acrescente fatos externos.
- Não faça recomendações.
- Não diga que os textos representam todo o Brasil.
- Não use título ou lista.
- Escreva exatamente duas frases.
- Use no máximo 70 palavras.
- Escreva em português do Brasil.

A primeira frase deve começar:
"Os textos destacam"

A segunda frase deve começar:
"O levantamento também considera critérios como"

RESPOSTA:
'''.strip()

    try:
        resumo = gerar_resposta(prompt, max_new_tokens=120).strip()
        metodo_resumo = 'LLM - primeira resposta validada'

        if resumo_tem_extrapolacao(resumo):
            prompt_correcao = f'''
TEXTOS ORIGINAIS:

{textos_numerados}

RESPOSTA ANTERIOR:

{resumo}

A resposta anterior contém afirmações
que não podem ser confirmadas nos textos.

Reescreva a síntese.

REGRAS:
- Use somente informações explícitas.
- Não escreva "falta de rampas".
- Não escreva "problemas de calçadas".
- Não transforme critérios em problemas encontrados.
- Não invente ausências ou deficiências.
- Não faça recomendações.
- Use exatamente duas frases.
- Use no máximo 70 palavras.

A primeira frase deve começar:
"Os textos destacam"

A segunda frase deve começar:
"O levantamento também considera critérios como"

RESPOSTA CORRIGIDA:
'''.strip()
            resumo = gerar_resposta(prompt_correcao, max_new_tokens=120).strip()
            metodo_resumo = 'LLM - resposta corrigida'

        if resumo_tem_extrapolacao(resumo):
            resumo = gerar_resumo_seguro(categoria, trechos)
            metodo_resumo = 'Resumo de segurança baseado nas evidências'

        status = obter_status_modelo()
        return {
            'categoria': categoria,
            'quantidade_trechos': len(trechos),
            'modelo': status['modelo'],
            'dispositivo': status['dispositivo'],
            'metodo_resumo': metodo_resumo,
            'trechos': trechos,
            'resumo': resumo,
        }
    except (FileNotFoundError, OSError, RuntimeError) as erro:
        raise HTTPException(503, str(erro)) from erro
    except Exception as erro:
        raise HTTPException(500, 'Erro inesperado ao gerar a síntese dos textos.') from erro
