from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


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


app = FastAPI(
    title="API - Acessibilidade Urbana no Brasil",
    description=(
        "API simples para consultar os indicadores do projeto "
        "e registrar observações complementares."
    ),
    version="1.0.0",
)


class Observacao(BaseModel):
    Estado: str
    Observacao: str


def carregar_ibge():
    return pd.read_csv(CAMINHO_IBGE)


@app.get(
    "/",
    summary="Verificar a API",
)
def inicio():
    return {
        "mensagem": "API do projeto Acessibilidade Urbana no Brasil",
        "documentacao": "/docs",
    }


@app.get(
    "/ufs",
    summary="Listar todas as UFs",
)
def listar_ufs():
    df = carregar_ibge()
    return df.to_dict(orient="records")


@app.get(
    "/ufs/{estado}",
    summary="Consultar uma UF pelo nome",
)
def consultar_estado(estado: str):
    df = carregar_ibge()

    resultado = df[
        df["Estado"].str.casefold()
        == estado.casefold()
    ]

    if resultado.empty:
        raise HTTPException(
            status_code=404,
            detail="Estado não encontrado.",
        )

    return resultado.iloc[0].to_dict()


@app.post(
    "/observacoes",
    summary="Registrar uma observação complementar",
)
def adicionar_observacao(observacao: Observacao):
    df_ibge = carregar_ibge()

    estado_valido = (
        df_ibge["Estado"].str.casefold()
        == observacao.Estado.casefold()
    ).any()

    if not estado_valido:
        raise HTTPException(
            status_code=400,
            detail="Informe o nome de uma UF existente na base.",
        )

    novo_registro = pd.DataFrame(
        [observacao.model_dump()]
    )

    if CAMINHO_OBSERVACOES.exists():
        observacoes = pd.read_csv(
            CAMINHO_OBSERVACOES
        )

        observacoes = pd.concat(
            [observacoes, novo_registro],
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
        "mensagem": "Observação registrada com sucesso.",
        "dados": observacao.model_dump(),
    }


@app.get(
    "/observacoes",
    summary="Listar observações registradas",
)
def listar_observacoes():
    if not CAMINHO_OBSERVACOES.exists():
        return []

    df = pd.read_csv(CAMINHO_OBSERVACOES)
    return df.to_dict(orient="records")
