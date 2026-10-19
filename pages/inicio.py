import streamlit as st

from comum import carregar_dados_ibge


df = carregar_dados_ibge()


st.title("Acessibilidade Urbana no Brasil")

st.write(
    "Aplicação desenvolvida para organizar, visualizar e comparar "
    "dados relacionados à acessibilidade e ao conforto do pedestre "
    "no entorno urbano brasileiro."
)


st.header("Problema de negócio")

st.write(
    "Facilitar a consulta e a interpretação de indicadores de "
    "acessibilidade urbana, permitindo que gestores, estudantes, "
    "profissionais e cidadãos comparem as Unidades da Federação "
    "de forma simples e interativa."
)


st.header("Objetivo do TP3")

st.write(
    "O TP3 mantém a análise dos dados do IBGE e do Mobilize, "
    "mas reorganiza a aplicação em múltiplas páginas, acrescenta "
    "uma API em FastAPI, corrige a ausência de visualização de "
    "frequência de termos apontada no TP2 e prepara a arquitetura "
    "para futura integração com LLMs."
)


st.header("Fonte quantitativa principal")

st.write(
    "IBGE - Censo Demográfico 2022 - Características Urbanísticas "
    "do Entorno dos Domicílios - Tabela SIDRA 9584."
)


st.info(
    "Os percentuais do IBGE se referem às características observadas "
    "no entorno dos domicílios considerados no levantamento. Eles não "
    "devem ser interpretados diretamente como percentual de todas as "
    "ruas de cada estado."
)


st.header("Resumo da base")

col1, col2 = st.columns(2)

with col1:
    st.metric("Unidades da Federação", len(df))

with col2:
    st.metric("Regiões brasileiras", df["Regiao"].nunique())


st.subheader("Amostra dos dados")
st.dataframe(df.head())


st.header("Navegação")

st.write(
    "Use o menu lateral para acessar Panorama IBGE, Comparações, "
    "Referência Mobilize, Upload e Download e API e LLM."
)
