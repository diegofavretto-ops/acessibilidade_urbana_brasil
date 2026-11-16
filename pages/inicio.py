import streamlit as st

from comum import carregar_dados_ibge


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

df = carregar_dados_ibge()


# =========================================================
# 2. CABEÇALHO
# =========================================================

st.title(
    "Acessibilidade Urbana no Brasil"
)

st.subheader(
    "Indicadores urbanos, comparações e análise com IA local"
)

st.write(
    "Aplicação desenvolvida para organizar, visualizar e comparar "
    "dados relacionados às condições do entorno urbano brasileiro, "
    "com foco em aspectos que influenciam a circulação e o conforto "
    "dos pedestres."
)

st.divider()


# =========================================================
# 3. INDICADORES RÁPIDOS
# =========================================================

st.subheader(
    "Visão geral do projeto"
)

col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.metric(
        label="Unidades da Federação",
        value=len(df),
    )


with col2:

    st.metric(
        label="Regiões brasileiras",
        value=df["Regiao"].nunique(),
    )


with col3:

    st.metric(
        label="Fonte principal",
        value="IBGE",
    )


with col4:

    st.metric(
        label="Modelo local",
        value="Qwen 0.5B",
    )


st.caption(
    "Base principal: Censo Demográfico 2022 - "
    "Características Urbanísticas do Entorno dos Domicílios."
)


# =========================================================
# 4. OBJETIVO DO PROJETO
# =========================================================

st.divider()

st.header(
    "Sobre o projeto"
)


col_esquerda, col_direita = st.columns(
    2
)


with col_esquerda:

    st.subheader(
        "Problema"
    )

    st.write(
        "Indicadores urbanos estão disponíveis em bases públicas, "
        "mas nem sempre são simples de consultar e comparar."
    )

    st.write(
        "O projeto busca facilitar a leitura dessas informações "
        "por meio de uma interface interativa."
    )


with col_direita:

    st.subheader(
        "Objetivo"
    )

    st.write(
        "Permitir que estudantes, profissionais, gestores e "
        "cidadãos consultem e comparem indicadores das Unidades "
        "da Federação de forma simples."
    )

    st.write(
        "O projeto também utiliza uma API e um modelo de linguagem "
        "local para gerar resumos a partir dos dados selecionados."
    )


# =========================================================
# 5. FONTES
# =========================================================

st.divider()

st.header(
    "Fontes utilizadas"
)


col_ibge, col_mobilize = st.columns(
    2
)


with col_ibge:

    st.subheader(
        "IBGE"
    )

    st.write(
        "**Censo Demográfico 2022**"
    )

    st.write(
        "Características Urbanísticas do "
        "Entorno dos Domicílios."
    )

    st.write(
        "Tabela SIDRA 9584."
    )

    st.success(
        "Fonte quantitativa principal do projeto."
    )


with col_mobilize:

    st.subheader(
        "Mobilize Brasil"
    )

    st.write(
        "Dados complementares relacionados "
        "às condições das calçadas."
    )

    st.write(
        "As informações foram obtidas por "
        "Web Scraping."
    )

    st.info(
        "Fonte utilizada apenas como referência complementar."
    )


# =========================================================
# 6. CUIDADO METODOLÓGICO
# =========================================================

st.warning(
    "Os percentuais do IBGE representam características observadas "
    "no entorno dos domicílios considerados no levantamento. "
    "Eles não devem ser interpretados diretamente como percentual "
    "de todas as ruas de cada estado."
)


# =========================================================
# 7. PRINCIPAIS INDICADORES
# =========================================================

st.divider()

st.header(
    "Principais indicadores analisados"
)


col1, col2, col3 = st.columns(
    3
)


with col1:

    with st.container(
        border=True
    ):

        st.subheader(
            "Infraestrutura"
        )

        st.write(
            "• Calçada/passeio"
        )

        st.write(
            "• Rampas"
        )

        st.write(
            "• Via para bicicleta"
        )


with col2:

    with st.container(
        border=True
    ):

        st.subheader(
            "Circulação"
        )

        st.write(
            "• Calçadas sem obstáculos"
        )

        st.write(
            "• Ponto de ônibus/van"
        )

        st.write(
            "• Iluminação pública"
        )


with col3:

    with st.container(
        border=True
    ):

        st.subheader(
            "Ambiente urbano"
        )

        st.write(
            "• Arborização"
        )

        st.write(
            "• Condições do entorno"
        )

        st.write(
            "• Comparações entre UFs"
        )


# =========================================================
# 8. RECURSOS DA APLICAÇÃO
# =========================================================

st.divider()

st.header(
    "O que a aplicação permite fazer"
)


col1, col2 = st.columns(
    2
)


with col1:

    with st.container(
        border=True
    ):

        st.subheader(
            "Análise de dados"
        )

        st.write(
            "📊 Visualizar indicadores por estado"
        )

        st.write(
            "🔎 Comparar Unidades da Federação"
        )

        st.write(
            "🚶 Consultar referências do Mobilize"
        )

        st.write(
            "📈 Explorar tabelas e gráficos"
        )


with col2:

    with st.container(
        border=True
    ):

        st.subheader(
            "Integração"
        )

        st.write(
            "📁 Adicionar dados por arquivo CSV"
        )

        st.write(
            "🔗 Consultar dados pela FastAPI"
        )

        st.write(
            "🤖 Gerar resumos com IA local"
        )

        st.write(
            "💻 Executar o modelo no próprio computador"
        )


# =========================================================
# 9. COMO NAVEGAR
# =========================================================

st.divider()

st.header(
    "Explore a aplicação"
)

st.write(
    "Use o menu lateral para acessar cada etapa da análise."
)


col1, col2 = st.columns(
    2
)


with col1:

    with st.container(
        border=True
    ):

        st.subheader(
            "📊 Panorama IBGE"
        )

        st.write(
            "Consulte os principais indicadores "
            "das Unidades da Federação."
        )


    with st.container(
        border=True
    ):

        st.subheader(
            "🔎 Comparações"
        )

        st.write(
            "Compare estados, regiões e indicadores."
        )


    with st.container(
        border=True
    ):

        st.subheader(
            "🚶 Referências Web"
        )

        st.write(
            "Explore os dados complementares "
            "obtidos no Mobilize Brasil."
        )


with col2:

    with st.container(
        border=True
    ):

        st.subheader(
            "📁 Upload e Download"
        )

        st.write(
            "Adicione ou exporte dados "
            "complementares."
        )


    with st.container(
        border=True
    ):

        st.subheader(
            "🤖 API e LLM"
        )

        st.write(
            "Consulte a FastAPI e gere resumos "
            "com o modelo Qwen executado localmente."
        )


# =========================================================
# 10. CONTEXTO FINAL
# =========================================================

st.divider()

st.caption(
    "Projeto relacionado ao ODS 11 - "
    "Cidades e Comunidades Sustentáveis."
)