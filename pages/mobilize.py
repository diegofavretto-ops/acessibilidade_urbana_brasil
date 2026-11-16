from collections import Counter
import re

import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_mobilize,
    carregar_mobilize_panorama,
)


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

df_mobilize = carregar_dados_mobilize()
df_panorama = carregar_mobilize_panorama()


# =========================================================
# 2. TÍTULO E CONTEXTO
# =========================================================

st.title("Referência externa - Mobilize")

st.write(
    "Esta página apresenta dados complementares obtidos por "
    "Web Scraping no Mobilize Brasil, relacionados às condições "
    "das calçadas."
)

st.info(
    "Os dados do Mobilize possuem metodologia, período e unidade "
    "de análise diferentes dos dados do IBGE. Por isso, são usados "
    "como referência complementar e não são comparados diretamente "
    "com os percentuais do Censo 2022."
)


# =========================================================
# 3. CRITÉRIOS DO MOBILIZE
# =========================================================

criterios_mobilize = {
    "Irregularidades no piso": "Irregularidades",
    "Degraus": "Degraus",
    "Inclinação": "Inclinacao",
    "Largura": "Largura",
    "Rampas de acessibilidade": "Rampas",
    "Obstáculos": "Obstaculos",
    "Iluminação": "Iluminacao",
    "Arborização": "Arborizacao",
    "Sinalização": "Sinalizacao",
    "Nota média geral": "Media",
}


# =========================================================
# 4. ESTATÍSTICAS DAS AVALIAÇÕES
# =========================================================

st.header("1. Avaliações das calçadas")

st.write(
    "O levantamento atribui notas de 0 a 10 para diferentes "
    "critérios relacionados às condições das calçadas."
)


criterio_nome = st.selectbox(
    "Selecione um critério:",
    list(criterios_mobilize.keys()),
    key="mobilize_criterio",
)

criterio = criterios_mobilize[
    criterio_nome
]


st.caption(
    "Unidade de medida: nota de 0 a 10."
)


if criterio == "Irregularidades":

    st.info(
        "A nota de irregularidades representa a avaliação "
        "das condições do piso. Ela não corresponde à "
        "quantidade de irregularidades encontradas."
    )


media = df_mobilize[
    criterio
].mean()


quantidade_avaliacoes = (
    df_mobilize[
        criterio
    ]
    .notna()
    .sum()
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Nota média",
        f"{media:.2f} / 10",
    )


with col2:

    st.metric(
        "Locais com nota válida",
        quantidade_avaliacoes,
    )


ranking = (
    df_mobilize[
        [
            "Endereco",
            "Cidade",
            criterio,
        ]
    ]
    .dropna(
        subset=[criterio]
    )
    .rename(
        columns={
            "Endereco":
                "Endereço",

            "Cidade":
                "Cidade/localidade",

            criterio:
                "Nota (0 a 10)",
        }
    )
)


# =========================================================
# 5. RANKINGS
# =========================================================

st.subheader(
    "Destaques do critério selecionado"
)


aba_maiores, aba_menores = st.tabs(
    [
        "5 maiores notas",
        "5 menores notas",
    ]
)


with aba_maiores:

    maiores_notas = (
        ranking
        .nlargest(
            5,
            "Nota (0 a 10)",
        )
        .reset_index(
            drop=True
        )
    )

    st.dataframe(
        maiores_notas,
        use_container_width=True,
        hide_index=True,
    )


with aba_menores:

    menores_notas = (
        ranking
        .nsmallest(
            5,
            "Nota (0 a 10)",
        )
        .reset_index(
            drop=True
        )
    )

    st.dataframe(
        menores_notas,
        use_container_width=True,
        hide_index=True,
    )


with st.expander(
    "Ver todos os dados raspados"
):

    st.dataframe(
        df_mobilize,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 6. VISÃO GERAL DOS CRITÉRIOS
# =========================================================

st.header(
    "2. Comparação entre os critérios"
)

st.write(
    "O gráfico abaixo compara a nota média obtida em cada "
    "critério do levantamento."
)


criterios_comparacao = {
    "Irregularidades no piso":
        "Irregularidades",

    "Degraus":
        "Degraus",

    "Inclinação":
        "Inclinacao",

    "Largura":
        "Largura",

    "Rampas de acessibilidade":
        "Rampas",

    "Obstáculos":
        "Obstaculos",

    "Iluminação":
        "Iluminacao",

    "Arborização":
        "Arborizacao",

    "Sinalização":
        "Sinalizacao",
}


dados_medias = []


for nome, coluna in (
    criterios_comparacao.items()
):

    dados_medias.append(
        {
            "Critério":
                nome,

            "Nota média":
                round(
                    df_mobilize[
                        coluna
                    ].mean(),
                    2,
                ),
        }
    )


df_medias = pd.DataFrame(
    dados_medias
)


df_medias = (
    df_medias
    .sort_values(
        "Nota média",
        ascending=False,
    )
    .reset_index(
        drop=True
    )
)


st.bar_chart(
    df_medias,
    x="Critério",
    y="Nota média",
    horizontal=True,
    sort="-Nota média",
    height=420,
    x_label="Critério",
    y_label="Nota média (0 a 10)",
    alt=(
        "Comparação das notas médias dos critérios "
        "avaliados pelo Mobilize."
    ),
)


with st.expander(
    "Ver valores das médias"
):

    st.dataframe(
        df_medias,
        use_container_width=True,
        hide_index=True,
    )


st.caption(
    "As notas pertencem exclusivamente ao levantamento "
    "do Mobilize e não devem ser comparadas diretamente "
    "com os percentuais do IBGE."
)


# =========================================================
# 7. ANÁLISE TEXTUAL
# =========================================================

st.header(
    "3. Termos recorrentes no Panorama das Calçadas"
)

st.write(
    "Para complementar as avaliações numéricas, esta análise "
    "utiliza os textos coletados na segunda página do Mobilize. "
    "Assim, a frequência representa palavras presentes no conteúdo "
    "sobre as condições das calçadas, e não nomes de ruas ou cidades."
)


texto_panorama = " ".join(
    df_panorama[
        "Texto"
    ]
    .fillna("")
    .astype(str)
    .tolist()
)


palavras = re.findall(
    r"[A-Za-zÀ-ÿ]+",
    texto_panorama.lower(),
)


# Palavras funcionais muito comuns que não ajudam
# na interpretação do conteúdo.
palavras_excluidas = {
    "aos",
    "ainda",
    "alguma",
    "algumas",
    "alguns",
    "assim",
    "cada",
    "com",
    "como",
    "contra",
    "das",
    "deve",
    "devem",
    "dos",
    "ela",
    "elas",
    "ele",
    "eles",
    "entre",
    "essa",
    "essas",
    "esse",
    "esses",
    "esta",
    "estas",
    "este",
    "estes",
    "foram",
    "mais",
    "mesmo",
    "muito",
    "muitos",
    "muita",
    "muitas",
    "nas",
    "não",
    "nos",
    "onde",
    "outra",
    "outras",
    "outro",
    "outros",
    "para",
    "pela",
    "pelas",
    "pelo",
    "pelos",
    "pode",
    "podem",
    "pois",
    "por",
    "quando",
    "que",
    "são",
    "sem",
    "sendo",
    "ser",
    "seu",
    "seus",
    "sua",
    "suas",
    "sobre",
    "também",
    "tem",
    "ter",
    "uma",
    "umas",
    "uns",
}


palavras_filtradas = []


for palavra in palavras:

    if (
        len(palavra) >= 4
        and palavra
        not in palavras_excluidas
    ):

        palavras_filtradas.append(
            palavra
        )


contador = Counter(
    palavras_filtradas
)


quantidade_termos = st.selectbox(
    "Quantidade de termos exibidos:",
    [
        10,
        15,
        20,
    ],
    index=0,
    key="mobilize_qtd_termos",
)


mais_frequentes = (
    contador
    .most_common(
        quantidade_termos
    )
)


if mais_frequentes:

    df_frequencia = pd.DataFrame(
        mais_frequentes,
        columns=[
            "Termo",
            "Frequência",
        ],
    )


    st.bar_chart(
        df_frequencia,
        x="Termo",
        y="Frequência",
        horizontal=True,
        sort="-Frequência",
        height=420,
        x_label="Termo",
        y_label="Frequência",
        alt=(
            "Termos mais frequentes nos textos coletados "
            "na página Panorama das Calçadas."
        ),
    )


    with st.expander(
        "Ver frequência em tabela"
    ):

        st.dataframe(
            df_frequencia,
            use_container_width=True,
            hide_index=True,
        )


    st.caption(
        "Palavras funcionais muito comuns foram removidas "
        "para facilitar a leitura dos temas presentes nos textos."
    )


else:

    st.warning(
        "Não há conteúdo textual suficiente para "
        "calcular a frequência."
    )


# =========================================================
# 8. PANORAMA TEXTUAL DAS CALÇADAS
# =========================================================

st.header(
    "4. Panorama textual das calçadas"
)

st.write(
    "A segunda coleta do Mobilize reúne trechos relacionados "
    "a diferentes aspectos das condições das calçadas."
)


st.caption(
    "Fonte complementar: Mobilize Brasil - "
    "Panorama das Calçadas."
)


categorias_panorama = (
    df_panorama[
        "Categorias"
    ]
    .str.split("; ")
    .explode()
    .dropna()
    .drop_duplicates()
    .sort_values()
    .tolist()
)


categoria_escolhida = st.selectbox(
    "Filtrar os textos por categoria:",
    [
        "Todas"
    ]
    + categorias_panorama,
    key="mobilize_panorama_categoria",
)


if categoria_escolhida == "Todas":

    df_filtrado = (
        df_panorama.copy()
    )

else:

    df_filtrado = df_panorama[
        df_panorama[
            "Categorias"
        ]
        .str.contains(
            categoria_escolhida,
            regex=False,
            na=False,
        )
    ]


st.metric(
    "Trechos encontrados",
    len(df_filtrado),
)


st.dataframe(
    df_filtrado[
        [
            "Categorias",
            "Texto",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)


# =========================================================
# 9. FREQUÊNCIA DAS CATEGORIAS
# =========================================================

st.subheader(
    "Categorias mais mencionadas"
)


frequencia_categorias = (
    df_panorama[
        "Categorias"
    ]
    .str.split("; ")
    .explode()
    .value_counts()
    .rename_axis(
        "Categoria"
    )
    .reset_index(
        name="Frequência"
    )
)


st.bar_chart(
    frequencia_categorias,
    x="Categoria",
    y="Frequência",
    horizontal=True,
    sort="-Frequência",
    height=420,
    x_label="Categoria",
    y_label="Quantidade de trechos",
    alt=(
        "Quantidade de trechos coletados que mencionam "
        "cada categoria relacionada às condições das calçadas."
    ),
)


with st.expander(
    "Ver frequência das categorias em tabela"
):

    st.dataframe(
        frequencia_categorias,
        use_container_width=True,
        hide_index=True,
    )


st.caption(
    "Um mesmo trecho pode mencionar mais de uma categoria. "
    "Por isso, a soma das frequências pode ser maior que "
    "a quantidade total de trechos coletados."
)