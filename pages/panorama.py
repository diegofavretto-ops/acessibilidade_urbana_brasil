import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_ibge,
    indicadores,
    indicadores_principais,
)


df = carregar_dados_ibge()


st.title("Panorama IBGE")

st.write(
    "Nesta página os indicadores do IBGE são apresentados em percentual (%)."
)


st.header("1. Visão nacional")

indicador_nacional = st.selectbox(
    "Selecione um indicador:",
    list(indicadores.keys()),
    key="panorama_indicador_nacional",
)

coluna_nacional = indicadores[indicador_nacional]

ranking = (
    df[["Estado", coluna_nacional]]
    .sort_values(coluna_nacional, ascending=False)
    .reset_index(drop=True)
)

ranking["Posição"] = range(1, len(ranking) + 1)

ranking = ranking[
    ["Posição", "Estado", coluna_nacional]
].rename(
    columns={coluna_nacional: "Percentual (%)"}
)

st.subheader(f"Ranking das UFs - {indicador_nacional}")
st.caption("Unidade de medida: percentual (%).")
st.dataframe(ranking)

st.bar_chart(
    ranking[["Estado", "Percentual (%)"]]
    .set_index("Estado")
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("5 maiores percentuais")
    st.dataframe(ranking.head(5))

with col2:
    st.subheader("5 menores percentuais")
    st.dataframe(ranking.tail(5))


st.header("2. Perfil de uma Unidade da Federação")

regioes = sorted(df["Regiao"].unique())

regiao_selecionada = st.selectbox(
    "Selecione a região:",
    regioes,
    key="panorama_regiao",
)


df_regiao = df[
    df["Regiao"] == regiao_selecionada
]

estados_regiao = sorted(
    df_regiao["Estado"].unique()
)

estado_selecionado = st.selectbox(
    "Selecione o estado:",
    estados_regiao,
    key="panorama_estado",
)


dados_estado = df[
    df["Estado"] == estado_selecionado
].iloc[0]

perfil = []

for nome, coluna in indicadores_principais.items():
    ranking_coluna = df[coluna].rank(
        ascending=False,
        method="min",
    )

    indice_estado = df[
        df["Estado"] == estado_selecionado
    ].index[0]

    posicao = int(
        ranking_coluna[indice_estado]
    )

    perfil.append(
        {
            "Indicador": nome,
            "Percentual (%)": dados_estado[coluna],
            "Posição entre as UFs": posicao,
        }
    )


df_perfil = pd.DataFrame(perfil)

df_perfil["Percentual (%)"] = (
    df_perfil["Percentual (%)"].round(1)
)

st.subheader(f"Perfil de {estado_selecionado}")
st.dataframe(df_perfil)

st.bar_chart(
    df_perfil[
        ["Indicador", "Percentual (%)"]
    ].set_index("Indicador")
)
