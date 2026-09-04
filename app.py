import pandas as pd
import streamlit as st


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

@st.cache_data
def carregar_dados_ibge():

    return pd.read_csv(
        "02_data_acquisition_understanding/ufs_streamlit_resumo.csv"
    )


@st.cache_data
def carregar_dados_mobilize():

    return pd.read_csv(
        "data/calcadas_mobilize.csv"
    )


df = carregar_dados_ibge()

df_mobilize = carregar_dados_mobilize()


# =========================================================
# 2. SESSION STATE
# =========================================================

if "dados_upload" not in st.session_state:

    st.session_state["dados_upload"] = None


# =========================================================
# 3. INDICADORES DO IBGE
# =========================================================

indicadores = {

    "Iluminação pública":
        "Iluminacao_publica_pct",

    "Ponto de ônibus/van":
        "Ponto_onibus_van_pct",

    "Via para bicicleta":
        "Via_bicicleta_pct",

    "Calçada/passeio":
        "Calcada_passeio_pct",

    "Calçadas sem obstáculos":
        "Calcadas_sem_obstaculos_pct",

    "Rampas":
        "Rampas_pct",

    "Arborização":
        "Arborizacao_com_arvores_pct"
}


indicadores_principais = {

    "Calçada/passeio":
        "Calcada_passeio_pct",

    "Calçadas sem obstáculos":
        "Calcadas_sem_obstaculos_pct",

    "Rampas":
        "Rampas_pct",

    "Arborização":
        "Arborizacao_com_arvores_pct"
}


# =========================================================
# 4. APRESENTAÇÃO
# =========================================================

st.title(
    "Acessibilidade Urbana no Brasil"
)


st.header(
    "Problema de negócio"
)


st.write("""
Identificar e analisar os problemas de acessibilidade urbana no Brasil,
com foco nas características do entorno dos domicílios relacionadas
à circulação de pedestres, acessibilidade e conforto urbano.

O objetivo é organizar os dados de forma simples e interativa,
permitindo comparar diferentes Unidades da Federação e regiões
brasileiras.
""")


st.header(
    "Objetivo do projeto"
)


st.write("""
Analisar dados sobre acessibilidade urbana no Brasil, incluindo
infraestrutura dos passeios, transporte público, rampas,
obstáculos e arborização.
""")


st.write("""
**Fonte principal:** IBGE - Censo Demográfico 2022 -
Características Urbanísticas do Entorno dos Domicílios.
""")


st.info("""
Os indicadores do IBGE apresentados nesta aplicação representam
percentuais relacionados às características observadas no entorno
dos domicílios considerados no levantamento.

Eles não representam diretamente o percentual de todas as ruas
de cada estado.
""")


# =========================================================
# 5. VISÃO NACIONAL
# =========================================================

st.header(
    "1. Visão nacional"
)


indicador_nacional = st.selectbox(
    "Selecione um indicador para analisar:",
    list(
        indicadores.keys()
    )
)


coluna_nacional = indicadores[
    indicador_nacional
]


ranking = (
    df[
        [
            "Estado",
            coluna_nacional
        ]
    ]
    .sort_values(
        coluna_nacional,
        ascending=False
    )
    .reset_index(
        drop=True
    )
)


ranking["Posição"] = range(
    1,
    len(ranking) + 1
)


ranking = ranking[
    [
        "Posição",
        "Estado",
        coluna_nacional
    ]
]


ranking = ranking.rename(
    columns={
        coluna_nacional:
            "Percentual (%)"
    }
)


st.subheader(
    f"Ranking das UFs - {indicador_nacional}"
)


st.caption(
    "Unidade de medida: percentual (%)."
)


st.dataframe(
    ranking
)


grafico_ranking = (
    ranking[
        [
            "Estado",
            "Percentual (%)"
        ]
    ]
    .set_index(
        "Estado"
    )
)


st.bar_chart(
    grafico_ranking
)


st.subheader(
    "5 UFs com maiores percentuais"
)


st.dataframe(
    ranking.head(5)
)


st.subheader(
    "5 UFs com menores percentuais"
)


st.dataframe(
    ranking.tail(5)
)


# =========================================================
# 6. PERFIL DE UMA UF
# =========================================================

st.header(
    "2. Perfil de uma Unidade da Federação"
)


regioes = sorted(
    df["Regiao"].unique()
)


regiao_selecionada = st.selectbox(
    "Selecione a região:",
    regioes
)


df_regiao = df[
    df["Regiao"]
    == regiao_selecionada
]


estados_regiao = sorted(
    df_regiao["Estado"].unique()
)


estado_selecionado = st.selectbox(
    "Selecione o estado:",
    estados_regiao
)


dados_estado = df[
    df["Estado"]
    == estado_selecionado
].iloc[0]


perfil = []


for nome, coluna in indicadores_principais.items():

    ranking_coluna = (
        df[coluna]
        .rank(
            ascending=False,
            method="min"
        )
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
                dados_estado[coluna],

            "Posição entre as UFs":
                posicao
        }
    )


df_perfil = pd.DataFrame(
    perfil
)


st.subheader(
    f"Perfil de {estado_selecionado}"
)


st.caption(
    "Os valores dos indicadores são apresentados em percentual (%)."
)


st.dataframe(
    df_perfil
)


st.bar_chart(
    df_perfil[
        [
            "Indicador",
            "Percentual (%)"
        ]
    ]
    .set_index(
        "Indicador"
    )
)


# =========================================================
# 7. ESTADO × REGIÃO × MÉDIA DAS UFs
# =========================================================

st.header(
    "3. Estado × região × média das UFs"
)


comparacao = []


for nome, coluna in indicadores_principais.items():

    valor_estado = (
        dados_estado[coluna]
    )


    media_regiao = (
        df_regiao[coluna]
        .mean()
    )


    media_ufs = (
        df[coluna]
        .mean()
    )


    comparacao.append(
        {
            "Indicador":
                nome,

            f"{estado_selecionado} (%)":
                valor_estado,

            f"Média das UFs - {regiao_selecionada} (%)":
                media_regiao,

            "Média das 27 UFs (%)":
                media_ufs
        }
    )


df_comparacao = pd.DataFrame(
    comparacao
)


df_comparacao = (
    df_comparacao.round(1)
)


st.caption(
    "Unidade de medida: percentual (%)."
)


st.dataframe(
    df_comparacao
)


st.bar_chart(
    df_comparacao.set_index(
        "Indicador"
    )
)


st.info("""
As médias apresentadas são médias simples dos percentuais
das Unidades da Federação.

Por exemplo, a média da Região Sul é calculada utilizando os
percentuais das UFs pertencentes à Região Sul.

Essas médias não representam um percentual nacional ponderado
pela população.
""")


# =========================================================
# 8. COMPARAÇÃO ENTRE DUAS UFs
# =========================================================

st.header(
    "4. Comparação entre duas UFs"
)


todos_estados = sorted(
    df["Estado"].unique()
)


estado_1 = st.selectbox(
    "Primeiro estado:",
    todos_estados,
    index=0
)


estado_2 = st.selectbox(
    "Segundo estado:",
    todos_estados,
    index=1
)


linha_estado_1 = df[
    df["Estado"]
    == estado_1
].iloc[0]


linha_estado_2 = df[
    df["Estado"]
    == estado_2
].iloc[0]


comparacao_estados = []


for nome, coluna in indicadores_principais.items():

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
                ]
        }
    )


df_comparacao_estados = pd.DataFrame(
    comparacao_estados
)


df_comparacao_estados = (
    df_comparacao_estados.round(1)
)


st.caption(
    "Unidade de medida: percentual (%)."
)


st.dataframe(
    df_comparacao_estados
)


st.bar_chart(
    df_comparacao_estados.set_index(
        "Indicador"
    )
)


# =========================================================
# 9. COMPARAÇÃO ENTRE REGIÕES
# =========================================================

st.header(
    "5. Comparação entre regiões"
)


indicador_regiao = st.selectbox(
    "Selecione o indicador para comparar as regiões:",
    list(
        indicadores.keys()
    )
)


coluna_regiao = indicadores[
    indicador_regiao
]


media_regioes = (
    df.groupby(
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


media_regioes = media_regioes.rename(
    columns={
        coluna_regiao:
            "Média dos percentuais das UFs (%)"
    }
)


media_regioes[
    "Média dos percentuais das UFs (%)"
] = (
    media_regioes[
        "Média dos percentuais das UFs (%)"
    ]
    .round(1)
)


st.subheader(
    f"Média regional - {indicador_regiao}"
)


st.caption(
    "Unidade de medida: média simples dos percentuais das UFs (%)."
)


st.dataframe(
    media_regioes
)


st.bar_chart(
    media_regioes.set_index(
        "Regiao"
    )
)


st.info("""
Cada valor representa a média simples dos percentuais das
Unidades da Federação pertencentes à respectiva região.

Portanto, esses valores não representam diretamente o percentual
de toda a população ou de todos os domicílios da região.
""")


# =========================================================
# 10. REFERÊNCIA EXTERNA - MOBILIZE
# =========================================================

st.header(
    "6. Referência externa sobre calçadas"
)


st.write("""
Os dados desta seção foram obtidos através de Web Scraping
a partir do levantamento **Calçadas do Brasil**, publicado
pelo Mobilize Brasil.

Os critérios do levantamento são apresentados através de
**notas de 0 a 10**.

Portanto, os números desta seção são notas de avaliação e
não percentuais.

Os dados possuem metodologia, período e unidade de análise
diferentes dos dados do IBGE e são utilizados somente como
referência complementar.
""")


# ---------------------------------------------------------
# CRITÉRIOS DO MOBILIZE
# ---------------------------------------------------------

criterios_mobilize = {

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

    "Nota média geral":
        "Media"
}


criterio_nome = st.selectbox(
    "Selecione um critério do levantamento Mobilize:",
    list(
        criterios_mobilize.keys()
    )
)


criterio_mobilize = criterios_mobilize[
    criterio_nome
]


st.caption(
    "Unidade de medida: nota de 0 a 10."
)


# ---------------------------------------------------------
# EXPLICAÇÃO ESPECIAL PARA IRREGULARIDADES
# ---------------------------------------------------------

if criterio_mobilize == "Irregularidades":

    st.info("""
    O valor de irregularidades representa uma nota atribuída
    ao critério relacionado às condições do piso.

    Portanto, o valor não representa a quantidade de
    irregularidades encontradas.
    """)


# ---------------------------------------------------------
# MÉDIA DO CRITÉRIO
# ---------------------------------------------------------

media_mobilize = (
    df_mobilize[
        criterio_mobilize
    ]
    .mean()
)


st.write(
    f"**Nota média dos locais avaliados: "
    f"{media_mobilize:.2f} / 10**"
)


# ---------------------------------------------------------
# DEFINE QUAL COLUNA SERÁ UTILIZADA COMO MUNICÍPIO
# ---------------------------------------------------------

if "Municipio" in df_mobilize.columns:

    coluna_municipio = "Municipio"

else:

    coluna_municipio = "Cidade"


# ---------------------------------------------------------
# RANKING DOS LOCAIS
# ---------------------------------------------------------

ranking_mobilize = (
    df_mobilize[
        [
            "Endereco",
            coluna_municipio,
            criterio_mobilize
        ]
    ]
    .dropna(
        subset=[
            criterio_mobilize
        ]
    )
    .sort_values(
        criterio_mobilize,
        ascending=False
    )
)


ranking_mobilize = ranking_mobilize.rename(
    columns={
        "Endereco":
            "Endereço",

        coluna_municipio:
            "Município",

        criterio_mobilize:
            "Nota (0 a 10)"
    }
)


st.subheader(
    "5 locais com maiores notas"
)


st.dataframe(
    ranking_mobilize.head(5)
)


st.subheader(
    "5 locais com menores notas"
)


st.dataframe(
    ranking_mobilize.tail(5)
)


# ---------------------------------------------------------
# MOSTRAR TODA A BASE
# ---------------------------------------------------------

mostrar_mobilize = st.checkbox(
    "Mostrar todos os dados coletados do Mobilize"
)


if mostrar_mobilize:

    st.dataframe(
        df_mobilize
    )


st.caption("""
As notas correspondem somente aos locais avaliados no
levantamento e não devem ser interpretadas como avaliação
de todas as calçadas de cada município.
""")


# =========================================================
# 11. UPLOAD DE DADOS
# =========================================================

st.header(
    "7. Adicionar dados complementares"
)


st.write("""
É possível enviar um arquivo CSV contendo informações
complementares sobre as Unidades da Federação.

O arquivo precisa possuir uma coluna chamada **Estado**.

As demais colunas serão acrescentadas à base principal.
""")


arquivo_enviado = st.file_uploader(
    "Selecione um arquivo CSV:",
    type=[
        "csv"
    ]
)


if arquivo_enviado is not None:

    try:

        dados_upload = pd.read_csv(
            arquivo_enviado
        )


        if "Estado" in dados_upload.columns:

            st.session_state[
                "dados_upload"
            ] = dados_upload


            st.success(
                "Arquivo carregado com sucesso."
            )


        else:

            st.error(
                "O arquivo precisa possuir "
                "uma coluna chamada Estado."
            )


    except Exception:

        st.error(
            "Não foi possível ler o arquivo CSV."
        )


# =========================================================
# 12. COMPLEMENTAÇÃO DOS DADOS
# =========================================================

df_complementado = df.copy()


if st.session_state[
    "dados_upload"
] is not None:

    st.subheader(
        "Dados enviados pelo usuário"
    )


    st.dataframe(
        st.session_state[
            "dados_upload"
        ]
    )


    df_complementado = (
        df.merge(
            st.session_state[
                "dados_upload"
            ],
            on="Estado",
            how="left"
        )
    )


    st.subheader(
        "Base com informações complementares"
    )


    st.dataframe(
        df_complementado
    )


# =========================================================
# 13. DOWNLOAD
# =========================================================

st.header(
    "8. Download dos dados"
)


csv_download = (
    df_complementado
    .to_csv(
        index=False
    )
    .encode(
        "utf-8-sig"
    )
)


st.download_button(
    label=
        "Baixar dados em CSV",

    data=
        csv_download,

    file_name=
        "dados_acessibilidade.csv",

    mime=
        "text/csv"
)


# =========================================================
# 14. FONTES DOS DADOS
# =========================================================

st.header(
    "Fontes dos dados"
)


st.write("""
**Fonte quantitativa principal**

IBGE - Censo Demográfico 2022 -
Características Urbanísticas do Entorno dos Domicílios.

Os indicadores desta base são apresentados em percentual (%).
""")


st.write("""
**Fonte complementar obtida por Web Scraping**

Mobilize Brasil - levantamento Calçadas do Brasil.

Os critérios desta base são apresentados como notas de 0 a 10.
""")


# =========================================================
# 15. REFERÊNCIAS
# =========================================================

st.header(
    "Referências e iniciativas relacionadas"
)


st.markdown("""
- [Manual Ilustrado de Calçadas de Curitiba](https://www.mobilize.org.br/midias/pesquisas/manual-ilustrado-de-calcadas-de-curitiba.pdf)

- [Diagnóstico de Caminhabilidade e Mobilidade a Pé no Brasil](https://www.mobilize.org.br/midias/pesquisas/diagostico-de-caminhabilidade-e-mobilidade-a-pe.pdf)

- [Calçadas do Brasil](https://www.mobilize.org.br/estatisticas/31/calcadas-do-brasil-ficam-com-media-34.html)

- [Relatório Calçadas do Brasil 2019](https://www.mobilize.org.br/Midias/Campanhas/Calcadas-2019/relatorio-final_v2.pdf)

- [Cidades de Pedestres - ITDP Brasil](https://itdpbrasil.org/wp-content/uploads/2018/12/Cidades-de-pedestres_FINAL_CCS.pdf)

- [Iniciativas públicas para caminhabilidade no Brasil](https://caosplanejado.com/3-melhores-iniciativas-publicas-para-caminhabilidade-no-brasil/)
""")


st.write("""
Essas referências são utilizadas como apoio para compreender
os diferentes aspectos relacionados à qualidade das calçadas,
acessibilidade e caminhabilidade.

Elas não alteram os indicadores utilizados na análise
quantitativa principal do projeto.
""")


st.write(
    "**Projeto relacionado ao ODS 11 - "
    "Cidades e Comunidades Sustentáveis.**"
)