
import streamlit as st

from comum import carregar_dados_ibge


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

df = carregar_dados_ibge()


# =========================================================
# 2. APRESENTAÇÃO DO PROJETO
# =========================================================

st.title("Acessibilidade Urbana no Brasil")

st.subheader(
    "Ciência de Dados e Inteligência Artificial "
    "aplicadas à acessibilidade urbana"
)

st.write(
    "Esta aplicação reúne indicadores públicos e informações "
    "coletadas na web para facilitar a análise das condições "
    "do ambiente urbano brasileiro, com foco na mobilidade "
    "e no conforto dos pedestres."
)

st.divider()


# =========================================================
# 3. VISÃO GERAL
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Unidades da Federação",
        df["Estado"].nunique(),
    )

with col2:

    st.metric(
        "Regiões brasileiras",
        df["Regiao"].nunique(),
    )

with col3:

    st.metric(
        "Fontes de dados",
        2,
    )

with col4:

    st.metric(
        "Modelo local",
        "Qwen 0.5B",
    )

st.caption(
    "Fonte principal: Censo Demográfico 2022 — "
    "Características Urbanísticas do Entorno dos Domicílios."
)


# =========================================================
# 4. PROBLEMA E OBJETIVO
# =========================================================

st.divider()

st.header("Sobre o projeto")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Problema")

    st.write(
        "Apesar da disponibilidade de dados públicos sobre "
        "as condições urbanas, a consulta e a comparação "
        "dessas informações nem sempre são simples."
    )

    st.write(
        "A dispersão dos dados dificulta a identificação "
        "de diferenças entre estados e regiões brasileiras."
    )

with col2:

    st.subheader("Objetivo")

    st.write(
        "Organizar e apresentar informações relacionadas "
        "à acessibilidade urbana em uma aplicação interativa, "
        "facilitando a consulta e a comparação dos indicadores."
    )

    st.write(
        "A Inteligência Artificial é utilizada como recurso "
        "complementar para interpretação dos dados e "
        "sumarização dos textos coletados."
    )


# =========================================================
# 5. FONTES DE DADOS
# =========================================================

st.divider()

st.header("Fontes de dados")

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("IBGE")

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

        st.write(
            "Fonte quantitativa principal utilizada "
            "para as comparações entre estados e regiões."
        )

        st.markdown(
            "[Consultar tabela SIDRA 9584]"
            "(https://sidra.ibge.gov.br/tabela/9584)"
        )

with col2:

    with st.container(border=True):

        st.subheader("Mobilize Brasil")

        st.write(
            "**Campanha Calçadas do Brasil**"
        )

        st.write(
            "Informações complementares sobre as condições "
            "das calçadas, obtidas por Web Scraping."
        )

        st.write(
            "Os textos coletados também são utilizados "
            "na funcionalidade de sumarização com IA."
        )

        st.markdown(
            "[Consultar Mobilize Brasil]"
            "(https://www.mobilize.org.br/)"
        )

st.caption(
    "As fontes possuem metodologias diferentes e devem "
    "ser interpretadas de forma complementar."
)


# =========================================================
# 6. PRINCIPAIS INDICADORES
# =========================================================

st.divider()

st.header("Indicadores analisados")

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("Infraestrutura")

        st.markdown(
            "- Calçada ou passeio\n"
            "- Rampas de acessibilidade\n"
            "- Via para bicicleta"
        )

with col2:

    with st.container(border=True):

        st.subheader("Circulação")

        st.markdown(
            "- Calçadas sem obstáculos\n"
            "- Ponto de ônibus ou van\n"
            "- Iluminação pública"
        )

with col3:

    with st.container(border=True):

        st.subheader("Ambiente urbano")

        st.markdown(
            "- Arborização\n"
            "- Características do entorno\n"
            "- Diferenças regionais"
        )

st.info(
    "Os percentuais do IBGE representam características "
    "observadas no entorno dos domicílios considerados "
    "na pesquisa, e não percentuais de todas as ruas "
    "de cada estado."
)


# =========================================================
# 7. RECURSOS DE INTELIGÊNCIA ARTIFICIAL
# =========================================================

st.divider()

st.header("Inteligência Artificial aplicada")

st.write(
    "O projeto utiliza o modelo de linguagem "
    "Qwen2.5-0.5B-Instruct, executado localmente "
    "e integrado à aplicação por meio da FastAPI."
)

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("Análise de indicadores")

        st.write(
            "O modelo recebe indicadores selecionados "
            "do IBGE e produz um resumo textual "
            "sobre a Unidade da Federação escolhida."
        )

        st.caption(
            "Disponível na página API e LLM."
        )

with col2:

    with st.container(border=True):

        st.subheader("Sumarização de textos")

        st.write(
            "O modelo recebe textos coletados do "
            "Mobilize Brasil e tenta produzir uma "
            "síntese relacionada à categoria selecionada."
        )

        st.caption(
            "Disponível na página Referências Web."
        )

st.caption(
    "As respostas da IA podem apresentar imprecisões. "
    "Os indicadores e os textos originais devem ser "
    "consultados para conferência."
)


# =========================================================
# 8. METODOLOGIA TDSP
# =========================================================

st.divider()

st.header("Metodologia de Ciência de Dados")

st.write(
    "O desenvolvimento foi organizado com base no "
    "Team Data Science Process (TDSP)."
)

etapas = [
    (
        "01",
        "Entendimento do negócio",
        "Definição do problema, dos objetivos "
        "e do contexto da acessibilidade urbana.",
    ),
    (
        "02",
        "Aquisição e entendimento dos dados",
        "Coleta, organização e análise dos dados "
        "do IBGE e do Mobilize Brasil.",
    ),
    (
        "03",
        "Modelagem",
        "Análise exploratória, integração do modelo "
        "de linguagem e Engenharia de Prompt.",
    ),
    (
        "04",
        "Implantação",
        "Integração do dashboard Streamlit, "
        "FastAPI e modelo local.",
    ),
    (
        "05",
        "Aceitação da solução",
        "Testes de funcionamento, análise dos resultados "
        "e identificação das limitações.",
    ),
]

for numero, titulo, descricao in etapas:

    with st.container(border=True):

        col_numero, col_descricao = st.columns([1, 9])

        with col_numero:

            st.subheader(numero)

        with col_descricao:

            st.markdown(f"**{titulo}**")

            st.write(descricao)


# =========================================================
# 9. ESG E ODS
# =========================================================

st.divider()

st.header("Sustentabilidade e inclusão urbana")

col1, col2 = st.columns(2)

with col1:

    st.subheader("ODS 11")

    st.write(
        "**Cidades e Comunidades Sustentáveis**"
    )

    st.write(
        "O projeto está relacionado à análise das condições "
        "urbanas e da mobilidade de pedestres, contribuindo "
        "para a discussão sobre cidades mais inclusivas "
        "e acessíveis."
    )

    st.markdown(
        "[Conhecer o ODS 11]"
        "(https://brasil.un.org/pt-br/sdgs/11)"
    )

with col2:

    st.subheader("ESG — Dimensão Social")

    st.write(
        "A acessibilidade urbana possui relação com "
        "inclusão social, mobilidade, segurança e "
        "qualidade de vida."
    )

    st.write(
        "A análise dos indicadores pode apoiar estudos "
        "e discussões sobre planejamento urbano e "
        "melhoria dos espaços públicos."
    )


# =========================================================
# 10. NAVEGAÇÃO
# =========================================================

st.divider()

st.header("Explore a aplicação")

st.write(
    "Utilize o menu lateral para acessar as funcionalidades."
)

paginas = [
    (
        "Panorama IBGE",
        "Consulte indicadores e rankings estaduais.",
    ),
    (
        "Comparações",
        "Compare estados, regiões e indicadores.",
    ),
    (
        "Referências Web",
        "Explore os dados do Mobilize e utilize "
        "a sumarização de textos com IA local.",
    ),
    (
        "Upload e Download",
        "Adicione ou exporte dados complementares.",
    ),
    (
        "API e LLM",
        "Consulte a API e gere resumos dos indicadores "
        "com Inteligência Artificial.",
    ),
]

for titulo, descricao in paginas:

    with st.container(border=True):

        st.markdown(f"**{titulo}**")

        st.write(descricao)


# =========================================================
# 11. IDENTIFICAÇÃO
# =========================================================

st.divider()

st.caption(
    "Diego Favretto | Ciência de Dados | "
    "Projeto de Bloco — Inteligência Artificial Aplicada"
)
