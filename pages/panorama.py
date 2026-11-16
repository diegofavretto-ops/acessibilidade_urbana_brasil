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

st.title("Panorama IBGE")

st.write(
    "Explore os indicadores do Censo Demográfico 2022 "
    "para as 27 Unidades da Federação."
)

st.info(
    "Os valores apresentados são percentuais relacionados às "
    "características observadas no entorno dos domicílios "
    "considerados pelo IBGE. Eles não representam diretamente "
    "o percentual de todas as ruas de cada estado."
)

st.divider()


# =========================================================
# 3. VISÃO NACIONAL
# =========================================================

st.header("1. Visão nacional")

indicador_nacional = st.selectbox(
    "Selecione um indicador:",
    list(indicadores.keys()),
    key="panorama_indicador_nacional",
)

coluna_nacional = indicadores[
    indicador_nacional
]


ranking = (
    df[
        [
            "Estado",
            coluna_nacional,
        ]
    ]
    .sort_values(
        coluna_nacional,
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)


ranking["Posição"] = range(
    1,
    len(ranking) + 1,
)


ranking = ranking[
    [
        "Posição",
        "Estado",
        coluna_nacional,
    ]
].rename(
    columns={
        coluna_nacional:
            "Percentual (%)",
    }
)


ranking[
    "Percentual (%)"
] = ranking[
    "Percentual (%)"
].round(1)


# =========================================================
# 4. RESUMO DO INDICADOR
# =========================================================

maior = ranking.iloc[0]
menor = ranking.iloc[-1]

media_nacional = ranking[
    "Percentual (%)"
].mean()


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Maior percentual",
        f"{maior['Percentual (%)']:.1f}%",
    )

    st.caption(
        maior["Estado"]
    )


with col2:

    st.metric(
        "Média das 27 UFs",
        f"{media_nacional:.1f}%",
    )

    st.caption(
        "Média simples dos percentuais."
    )


with col3:

    st.metric(
        "Menor percentual",
        f"{menor['Percentual (%)']:.1f}%",
    )

    st.caption(
        menor["Estado"]
    )


# =========================================================
# 5. GRÁFICO NACIONAL
# =========================================================

st.subheader(
    f"Ranking das UFs - {indicador_nacional}"
)

st.caption(
    "Unidade de medida: percentual (%)."
)


st.bar_chart(
    ranking,
    x="Estado",
    y="Percentual (%)",
    horizontal=True,
    sort="-Percentual (%)",
    height=700,
    x_label="Unidade da Federação",
    y_label="Percentual (%)",
    alt=(
        f"Ranking das Unidades da Federação para "
        f"{indicador_nacional}."
    ),
)


# =========================================================
# 6. MAIORES E MENORES
# =========================================================

aba_maiores, aba_menores = st.tabs(
    [
        "5 maiores percentuais",
        "5 menores percentuais",
    ]
)


with aba_maiores:

    st.dataframe(
        ranking.head(5),
        use_container_width=True,
        hide_index=True,
    )


with aba_menores:

    st.dataframe(
        ranking.tail(5),
        use_container_width=True,
        hide_index=True,
    )


with st.expander(
    "Ver ranking completo das 27 UFs"
):

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 7. PERFIL DE UMA UF
# =========================================================

st.divider()

st.header(
    "2. Perfil de uma Unidade da Federação"
)

st.write(
    "Selecione uma região e uma UF para visualizar "
    "os principais indicadores utilizados no projeto."
)


regioes = sorted(
    df["Regiao"].unique()
)


col_regiao, col_estado = st.columns(2)


with col_regiao:

    regiao_selecionada = st.selectbox(
        "Região:",
        regioes,
        key="panorama_regiao",
    )


df_regiao = df[
    df["Regiao"]
    == regiao_selecionada
]


estados_regiao = sorted(
    df_regiao[
        "Estado"
    ].unique()
)


with col_estado:

    estado_selecionado = st.selectbox(
        "Unidade da Federação:",
        estados_regiao,
        key="panorama_estado",
    )


dados_estado = df[
    df["Estado"]
    == estado_selecionado
].iloc[0]


# =========================================================
# 8. PERFIL E POSIÇÃO NACIONAL
# =========================================================

perfil = []


for nome, coluna in (
    indicadores_principais.items()
):

    ranking_coluna = df[
        coluna
    ].rank(
        ascending=False,
        method="min",
    )


    indice_estado = df[
        df["Estado"]
        == estado_selecionado
    ].index[0]


    posicao = int(
        ranking_coluna[
            indice_estado
        ]
    )


    perfil.append(
        {
            "Indicador":
                nome,

            "Percentual (%)":
                float(
                    dados_estado[
                        coluna
                    ]
                ),

            "Posição entre as UFs":
                posicao,
        }
    )


df_perfil = pd.DataFrame(
    perfil
)


df_perfil[
    "Percentual (%)"
] = df_perfil[
    "Percentual (%)"
].round(1)


st.subheader(
    f"Perfil de {estado_selecionado}"
)


# =========================================================
# 9. MÉTRICAS DO PERFIL
# =========================================================

colunas_metricas = st.columns(
    len(df_perfil)
)


for indice, linha in (
    df_perfil.iterrows()
):

    with colunas_metricas[
        indice
    ]:

        st.metric(
            linha["Indicador"],
            (
                f"{linha['Percentual (%)']:.1f}%"
            ),
        )

        st.caption(
            (
                f"{linha['Posição entre as UFs']}ª "
                "posição entre as UFs"
            )
        )


# =========================================================
# 10. GRÁFICO DO PERFIL
# =========================================================

st.bar_chart(
    df_perfil,
    x="Indicador",
    y="Percentual (%)",
    horizontal=True,
    sort=False,
    height=360,
    x_label="Indicador",
    y_label="Percentual (%)",
    alt=(
        f"Principais indicadores de "
        f"{estado_selecionado}."
    ),
)


with st.expander(
    "Ver detalhes do perfil"
):

    st.dataframe(
        df_perfil,
        use_container_width=True,
        hide_index=True,
    )