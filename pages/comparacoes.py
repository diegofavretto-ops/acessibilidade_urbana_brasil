import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_ibge,
    indicadores,
    indicadores_principais,
)


# =========================================================
# 1. DADOS
# =========================================================

df = carregar_dados_ibge()


# =========================================================
# 2. CABEÇALHO
# =========================================================

st.title("Comparações")

st.write(
    "Compare os principais indicadores entre uma UF, "
    "sua região, o conjunto das 27 UFs e outras "
    "Unidades da Federação."
)

st.info(
    "Os valores apresentados nesta página são percentuais "
    "relacionados às características observadas no entorno "
    "dos domicílios considerados pelo IBGE."
)

st.divider()


# =========================================================
# 3. UF × REGIÃO × BRASIL
# =========================================================

st.header(
    "1. UF × região × média das UFs"
)


regioes = sorted(
    df["Regiao"].unique()
)


col_regiao, col_estado = st.columns(
    2
)


with col_regiao:

    regiao = st.selectbox(
        "Região:",
        regioes,
        key="comparacao_regiao",
    )


df_regiao = df[
    df["Regiao"] == regiao
]


estados_regiao = sorted(
    df_regiao[
        "Estado"
    ].unique()
)


with col_estado:

    estado = st.selectbox(
        "Unidade da Federação:",
        estados_regiao,
        key="comparacao_estado",
    )


dados_estado = df[
    df["Estado"] == estado
].iloc[0]


comparacao = []


for nome, coluna in (
    indicadores_principais.items()
):

    comparacao.append(
        {
            "Indicador":
                nome,

            f"{estado} (%)":
                dados_estado[
                    coluna
                ],

            f"Média - {regiao} (%)":
                df_regiao[
                    coluna
                ].mean(),

            "Média das 27 UFs (%)":
                df[
                    coluna
                ].mean(),
        }
    )


df_comparacao = (
    pd.DataFrame(
        comparacao
    )
    .round(1)
)


st.subheader(
    f"{estado} em comparação com {regiao} e Brasil"
)


st.bar_chart(
    df_comparacao,
    x="Indicador",
    y=[
        f"{estado} (%)",
        f"Média - {regiao} (%)",
        "Média das 27 UFs (%)",
    ],
    horizontal=True,
    stack=False,
    sort=False,
    height=420,
    x_label="Indicador",
    y_label="Percentual (%)",
    alt=(
        f"Comparação entre {estado}, "
        f"a média de {regiao} e a média das 27 UFs."
    ),
)


with st.expander(
    "Ver valores da comparação"
):

    st.dataframe(
        df_comparacao,
        use_container_width=True,
        hide_index=True,
    )


st.info(
    "As médias regionais e a média das 27 UFs são "
    "médias simples dos percentuais das UFs. "
    "Não correspondem a um percentual ponderado "
    "pela população ou pelo número de domicílios."
)


# =========================================================
# 4. COMPARAÇÃO ENTRE DUAS UFs
# =========================================================

st.divider()

st.header(
    "2. Comparação entre duas UFs"
)


todos_estados = sorted(
    df["Estado"].unique()
)


col_uf1, col_uf2 = st.columns(
    2
)


with col_uf1:

    estado_1 = st.selectbox(
        "Primeira UF:",
        todos_estados,
        index=0,
        key="comparacao_estado_1",
    )


with col_uf2:

    estado_2 = st.selectbox(
        "Segunda UF:",
        todos_estados,
        index=1,
        key="comparacao_estado_2",
    )


if estado_1 == estado_2:

    st.warning(
        "Selecione duas Unidades da Federação "
        "diferentes para uma comparação mais útil."
    )


linha_estado_1 = df[
    df["Estado"] == estado_1
].iloc[0]


linha_estado_2 = df[
    df["Estado"] == estado_2
].iloc[0]


comparacao_estados = []


for nome, coluna in (
    indicadores_principais.items()
):

    comparacao_estados.append(
        {
            "Indicador":
                nome,

            f"{estado_1} (%)":
                linha_estado_1[
                    coluna
                ],

            f"{estado_2} (%)":
                linha_estado_2[
                    coluna
                ],
        }
    )


df_comparacao_estados = (
    pd.DataFrame(
        comparacao_estados
    )
    .round(1)
)


st.subheader(
    f"{estado_1} × {estado_2}"
)


st.bar_chart(
    df_comparacao_estados,
    x="Indicador",
    y=[
        f"{estado_1} (%)",
        f"{estado_2} (%)",
    ],
    horizontal=True,
    stack=False,
    sort=False,
    height=400,
    x_label="Indicador",
    y_label="Percentual (%)",
    alt=(
        f"Comparação dos principais indicadores "
        f"entre {estado_1} e {estado_2}."
    ),
)


with st.expander(
    "Ver valores da comparação entre as UFs"
):

    st.dataframe(
        df_comparacao_estados,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 5. COMPARAÇÃO ENTRE REGIÕES
# =========================================================

st.divider()

st.header(
    "3. Comparação entre regiões"
)


indicador_regiao = st.selectbox(
    "Indicador para comparar as regiões:",
    list(indicadores.keys()),
    key="comparacao_indicador_regiao",
)


coluna_regiao = indicadores[
    indicador_regiao
]


media_regioes = (
    df
    .groupby(
        "Regiao"
    )[
        coluna_regiao
    ]
    .mean()
    .sort_values(
        ascending=False
    )
    .reset_index()
)


media_regioes = (
    media_regioes.rename(
        columns={
            coluna_regiao:
                "Média (%)"
        }
    )
)


media_regioes[
    "Média (%)"
] = media_regioes[
    "Média (%)"
].round(1)


maior_regiao = media_regioes.iloc[0]
menor_regiao = media_regioes.iloc[-1]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Maior média regional",
        (
            f"{maior_regiao['Média (%)']:.1f}%"
        ),
    )

    st.caption(
        maior_regiao[
            "Regiao"
        ]
    )


with col2:

    st.metric(
        "Menor média regional",
        (
            f"{menor_regiao['Média (%)']:.1f}%"
        ),
    )

    st.caption(
        menor_regiao[
            "Regiao"
        ]
    )


st.bar_chart(
    media_regioes,
    x="Regiao",
    y="Média (%)",
    horizontal=True,
    sort="-Média (%)",
    height=330,
    x_label="Região",
    y_label="Média dos percentuais das UFs (%)",
    alt=(
        f"Comparação das regiões brasileiras para "
        f"{indicador_regiao}."
    ),
)


with st.expander(
    "Ver médias das regiões"
):

    st.dataframe(
        media_regioes,
        use_container_width=True,
        hide_index=True,
    )


st.caption(
    "As médias regionais apresentadas são médias simples "
    "dos percentuais das UFs pertencentes a cada região."
)