from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent

CAMINHO_IBGE = (
    BASE_DIR
    / "02_data_acquisition_understanding"
    / "ufs_streamlit_resumo.csv"
)

CAMINHO_MOBILIZE = (
    BASE_DIR
    / "data"
    / "calcadas_mobilize.csv"
)

CAMINHO_TEXTO_MOBILIZE = (
    BASE_DIR
    / "data"
    / "texto_mobilize.txt"
)


@st.cache_data
def carregar_dados_ibge():
    return pd.read_csv(CAMINHO_IBGE)


@st.cache_data
def carregar_dados_mobilize():
    return pd.read_csv(CAMINHO_MOBILIZE)


@st.cache_data
def carregar_texto_mobilize():
    if CAMINHO_TEXTO_MOBILIZE.exists():
        return CAMINHO_TEXTO_MOBILIZE.read_text(
            encoding="utf-8"
        )

    # Fallback: usa os campos textuais já raspados do CSV.
    df_mobilize = carregar_dados_mobilize()

    partes = []

    for coluna in ["Endereco", "Cidade"]:
        if coluna in df_mobilize.columns:
            partes.extend(
                df_mobilize[coluna]
                .dropna()
                .astype(str)
                .tolist()
            )

    return "\n".join(partes)


def inicializar_estado():
    if "dados_upload" not in st.session_state:
        st.session_state["dados_upload"] = None


indicadores = {
    "Iluminação pública": "Iluminacao_publica_pct",
    "Ponto de ônibus/van": "Ponto_onibus_van_pct",
    "Via para bicicleta": "Via_bicicleta_pct",
    "Calçada/passeio": "Calcada_passeio_pct",
    "Calçadas sem obstáculos": "Calcadas_sem_obstaculos_pct",
    "Rampas": "Rampas_pct",
    "Arborização": "Arborizacao_com_arvores_pct",
}


indicadores_principais = {
    "Calçada/passeio": "Calcada_passeio_pct",
    "Calçadas sem obstáculos": "Calcadas_sem_obstaculos_pct",
    "Rampas": "Rampas_pct",
    "Arborização": "Arborizacao_com_arvores_pct",
}
