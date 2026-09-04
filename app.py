import streamlit as st
import pandas as pd

st.title("Acessibilidade Urbana no Brasil")

st.header("Problema de negócio")

st.write("""
Identificar e analisar os problemas de acessibilidade urbana no Brasil, com foco em como as cidades estão se adaptando para atender às necessidades de todos os cidadãos, incluindo pessoas com deficiência e mobilidade reduzida. O objetivo é fornecer insights que possam orientar políticas públicas e iniciativas de planejamento urbano para promover cidades mais inclusivas e acessíveis.
""")

st.header("Objetivos do projeto")

st.write("""
- Analisar dados sobre acessibilidade urbana no Brasil, incluindo infraestrutura dos passeios, transporte público e arborização.
""")

st.header("Amostra dos dados")

df = pd.read_csv(
    "02_data_acquisition_understanding/ufs_streamlit_resumo.csv"
)

st.dataframe(df.head())

st.write("""
A tabela acima apresenta uma amostra dos dados do Censo 2022 do IBGE
que serão utilizados ao longo do projeto. Os indicadores representam
características do entorno dos domicílios relacionadas à acessibilidade
das calçadas e ao conforto do pedestre.
""")

st.header("Links úteis")

st.markdown("""
- [IBGE](https://www.ibge.gov.br/)
- [SIDRA](https://sidra.ibge.gov.br/)
- [ODS 11 - ONU](https://brasil.un.org/pt-br/sdgs/11)
""")