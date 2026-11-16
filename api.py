from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from llm_local import (
    gerar_resposta,
    obter_status_modelo,
)


# =========================================================
# 1. CAMINHOS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

CAMINHO_IBGE = (
    BASE_DIR
    / "02_data_acquisition_understanding"
    / "ufs_streamlit_resumo.csv"
)

CAMINHO_OBSERVACOES = (
    BASE_DIR
    / "data"
    / "observacoes_api.csv"
)


# =========================================================
# 2. APLICAÇÃO FASTAPI
# =========================================================

app = FastAPI(
    title="API - Acessibilidade Urbana no Brasil",
    description=(
        "API para consultar indicadores de acessibilidade urbana, "
        "registrar observações e gerar resumos com um LLM local."
    ),
    version="2.0.0",
)


# =========================================================
# 3. MODELOS PYDANTIC
# =========================================================

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
    Estado: str = Field(
        min_length=2,
        max_length=50,
    )

    Observacao: str = Field(
        min_length=1,
        max_length=500,
    )


class ObservacaoResposta(BaseModel):
    mensagem: str
    dados: Observacao


class StatusIAResposta(BaseModel):
    modelo: str
    dispositivo: str
    arquivos_locais: bool


class ResumoUFEntrada(BaseModel):
    estado: str = Field(
        min_length=2,
        max_length=50,
    )


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


# =========================================================
# 4. FUNÇÕES DE APOIO
# =========================================================

def carregar_ibge():
    return pd.read_csv(
        CAMINHO_IBGE
    )


def buscar_estado(
    estado: str,
):

    df = carregar_ibge()

    resultado = df[
        df["Estado"].str.casefold()
        == estado.strip().casefold()
    ]

    if resultado.empty:

        raise HTTPException(
            status_code=404,
            detail="Estado não encontrado.",
        )

    return resultado.iloc[0]


# =========================================================
# 5. ROTA INICIAL
# =========================================================

@app.get(
    "/",
    response_model=InicioResposta,
    summary="Verificar a API",
)
def inicio():

    return {
        "mensagem": (
            "API do projeto "
            "Acessibilidade Urbana no Brasil"
        ),
        "documentacao": "/docs",
    }


# =========================================================
# 6. ROTAS DOS DADOS DO IBGE
# =========================================================

@app.get(
    "/ufs",
    response_model=list[UFResposta],
    summary="Listar todas as UFs",
)
def listar_ufs():

    df = carregar_ibge()

    return df.to_dict(
        orient="records"
    )


@app.get(
    "/ufs/{estado}",
    response_model=UFResposta,
    summary="Consultar uma UF pelo nome",
)
def consultar_estado(
    estado: str,
):

    resultado = buscar_estado(
        estado
    )

    return resultado.to_dict()


# =========================================================
# 7. ROTAS DE OBSERVAÇÕES
# =========================================================

@app.post(
    "/observacoes",
    response_model=ObservacaoResposta,
    summary="Registrar uma observação complementar",
)
def adicionar_observacao(
    observacao: Observacao,
):

    df_ibge = carregar_ibge()

    estado_valido = (
        df_ibge["Estado"]
        .str.casefold()
        == observacao.Estado
        .strip()
        .casefold()
    ).any()

    if not estado_valido:

        raise HTTPException(
            status_code=400,
            detail=(
                "Informe o nome de uma UF "
                "existente na base."
            ),
        )

    novo_registro = pd.DataFrame(
        [
            observacao.model_dump()
        ]
    )

    if CAMINHO_OBSERVACOES.exists():

        observacoes = pd.read_csv(
            CAMINHO_OBSERVACOES
        )

        observacoes = pd.concat(
            [
                observacoes,
                novo_registro,
            ],
            ignore_index=True,
        )

    else:

        observacoes = novo_registro

    observacoes.to_csv(
        CAMINHO_OBSERVACOES,
        index=False,
        encoding="utf-8-sig",
    )

    return {
        "mensagem": (
            "Observação registrada "
            "com sucesso."
        ),
        "dados": observacao,
    }


@app.get(
    "/observacoes",
    response_model=list[Observacao],
    summary="Listar observações registradas",
)
def listar_observacoes():

    if not CAMINHO_OBSERVACOES.exists():
        return []

    df = pd.read_csv(
        CAMINHO_OBSERVACOES
    )

    return df.to_dict(
        orient="records"
    )


# =========================================================
# 8. STATUS DO LLM LOCAL
# =========================================================

@app.get(
    "/ia/status",
    response_model=StatusIAResposta,
    summary="Verificar o modelo local",
)
def status_ia():

    return obter_status_modelo()


# =========================================================
# 9. RESUMO DE UMA UF COM O LLM
# =========================================================

@app.post(
    "/ia/resumo-uf",
    response_model=ResumoUFResposta,
    summary="Gerar resumo de uma UF com IA local",
)
def gerar_resumo_uf(
    entrada: ResumoUFEntrada,
):

    estado = buscar_estado(
        entrada.estado
    )

    indicadores = {
        "calcada_passeio_pct": float(
            estado["Calcada_passeio_pct"]
        ),
        "calcadas_sem_obstaculos_pct": float(
            estado[
                "Calcadas_sem_obstaculos_pct"
            ]
        ),
        "rampas_pct": float(
            estado["Rampas_pct"]
        ),
        "arborizacao_com_arvores_pct": float(
            estado[
                "Arborizacao_com_arvores_pct"
            ]
        ),
    }

    prompt = f"""
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
6. Os indicadores representam características observadas no
   entorno dos domicílios considerados na pesquisa.
7. Calçadas sem obstáculos e rampas devem ser interpretadas
   dentro do contexto em que existe calçada.
8. Escreva em português do Brasil.
9. Produza no máximo quatro frases.
10. Destaque os principais valores sem criar um índice geral
    de acessibilidade.

Produza um resumo objetivo.
""".strip()

    try:

        resumo = gerar_resposta(
            prompt,
            max_new_tokens=80,
        )

    except FileNotFoundError as erro:

        raise HTTPException(
            status_code=503,
            detail=(
                "O modelo local não está "
                "disponível no servidor."
            ),
        ) from erro

    except (OSError, RuntimeError) as erro:

        raise HTTPException(
            status_code=503,
            detail=(
                "Não foi possível carregar "
                "ou executar o modelo local."
            ),
        ) from erro

    except Exception as erro:

        raise HTTPException(
            status_code=500,
            detail=(
                "Ocorreu um erro inesperado "
                "durante a geração do resumo."
            ),
        ) from erro

    status = obter_status_modelo()

    return {
        "estado": estado["Estado"],
        "regiao": estado["Regiao"],
        "modelo": status["modelo"],
        "dispositivo": status["dispositivo"],
        "indicadores": indicadores,
        "resumo": resumo,
    }