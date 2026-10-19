import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_ibge,
    indicadores,
    indicadores_principais,
)


df = carregar_dados_ibge()


st.title("Comparações")

st.caption(
    "Os valores do IBGE apresentados nesta página estão em percentual (%)."
)


st.header("1. UF × região × média das UFs")

regioes = sorted(df["Regiao"].unique())

regiao = st.selectbox(
    "Região:",
    regioes,
    key="comparacao_regiao",
)


df_regiao = df[
    df["Regiao"] == regiao
]

estados_regiao = sorted(
    df_regiao["Estado"].unique()
)

estado = st.selectbox(
    "Estado:",
    estados_regiao,
    key="comparacao_estado",
)


dados_estado = df[
    df["Estado"] == estado
].iloc[0]

comparacao = []

for nome, coluna in indicadores_principais.items():
    comparacao.append(
        {
            "Indicador": nome,
            f"{estado} (%)": dados_estado[coluna],
            f"Média das UFs - {regiao} (%)": df_regiao[coluna].mean(),
            "Média das 27 UFs (%)": df[coluna].mean(),
        }
    )


df_comparacao = pd.DataFrame(comparacao).round(1)

st.dataframe(df_comparacao)
st.bar_chart(df_comparacao.set_index("Indicador"))

st.info(
    "As médias regionais e a média das 27 UFs são médias simples "
    "dos percentuais das UFs. Não correspondem a um percentual "
    "ponderado pela população ou pelo número de domicílios."
)


st.header("2. Comparação entre duas UFs")

todos_estados = sorted(df["Estado"].unique())

estado_1 = st.selectbox(
    "Primeira UF:",
    todos_estados,
    index=0,
    key="comparacao_estado_1",
)

estado_2 = st.selectbox(
    "Segunda UF:",
    todos_estados,
    index=1,
    key="comparacao_estado_2",
)

linha_estado_1 = df[
    df["Estado"] == estado_1
].iloc[0]

linha_estado_2 = df[
    df["Estado"] == estado_2
].iloc[0]

comparacao_estados = []

for nome, coluna in indicadores_principais.items():
    comparacao_estados.append(
        {
            "Indicador": nome,
            f"{estado_1} (%)": linha_estado_1[coluna],
            f"{estado_2} (%)": linha_estado_2[coluna],
        }
    )


df_comparacao_estados = (
    pd.DataFrame(comparacao_estados).round(1)
)

st.dataframe(df_comparacao_estados)
st.bar_chart(
    df_comparacao_estados.set_index("Indicador")
)


st.header("3. Comparação entre regiões")

indicador_regiao = st.selectbox(
    "Indicador para comparar as regiões:",
    list(indicadores.keys()),
    key="comparacao_indicador_regiao",
)

coluna_regiao = indicadores[indicador_regiao]

media_regioes = (
    df.groupby("Regiao")[coluna_regiao]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

media_regioes = media_regioes.rename(
    columns={
        coluna_regiao: "Média dos percentuais das UFs (%)"
    }
)

media_regioes[
    "Média dos percentuais das UFs (%)"
] = media_regioes[
    "Média dos percentuais das UFs (%)"
].round(1)

st.dataframe(media_regioes)
st.bar_chart(media_regioes.set_index("Regiao"))
