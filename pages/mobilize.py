from collections import Counter
import re

import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_mobilize,
    carregar_texto_mobilize,
)


df_mobilize = carregar_dados_mobilize()
texto_mobilize = carregar_texto_mobilize()


st.title("Referência externa - Mobilize")

st.write(
    "Os dados desta página foram obtidos por Web Scraping a partir "
    "do levantamento Calçadas do Brasil, do Mobilize Brasil."
)

st.info(
    "Os critérios do Mobilize são notas de 0 a 10. Eles possuem "
    "metodologia, período e unidade de análise diferentes dos dados "
    "do IBGE e são usados somente como referência complementar."
)


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


st.header("1. Estatísticas das avaliações")

criterio_nome = st.selectbox(
    "Selecione um critério:",
    list(criterios_mobilize.keys()),
    key="mobilize_criterio",
)

criterio = criterios_mobilize[criterio_nome]

st.caption("Unidade de medida: nota de 0 a 10.")

if criterio == "Irregularidades":
    st.info(
        "Irregularidades é uma nota atribuída às condições do piso; "
        "não representa uma quantidade de irregularidades."
    )

media = df_mobilize[criterio].mean()

st.metric(
    "Nota média dos locais avaliados",
    f"{media:.2f} / 10",
)

ranking = (
    df_mobilize[
        ["Endereco", "Cidade", criterio]
    ]
    .dropna(subset=[criterio])
    .sort_values(criterio, ascending=False)
    .rename(
        columns={
            "Endereco": "Endereço",
            "Cidade": "Cidade/localidade",
            criterio: "Nota (0 a 10)",
        }
    )
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("5 maiores notas")
    st.dataframe(ranking.head(5))

with col2:
    st.subheader("5 menores notas")
    st.dataframe(ranking.tail(5))

mostrar_base = st.checkbox(
    "Mostrar todos os dados raspados"
)

if mostrar_base:
    st.dataframe(df_mobilize)


st.header("2. Frequência de termos")

st.write(
    "Esta visualização corrige a ausência apontada na avaliação do TP2. "
    "A contagem usa o conteúdo textual dos endereços e localidades "
    "obtidos no Web Scraping."
)

palavras = re.findall(
    r"[A-Za-zÀ-ÿ]+",
    texto_mobilize.lower(),
)

palavras_excluidas = {
    "para",
    "como",
    "mais",
    "pela",
    "pelo",
    "pelas",
    "pelos",
    "das",
    "dos",
    "uma",
    "com",
    "que",
    "não",
    "são",
    "nos",
    "nas",
    "por",
    "seu",
    "sua",
    "rua",
}

palavras_filtradas = []

for palavra in palavras:
    if (
        len(palavra) >= 4
        and palavra not in palavras_excluidas
    ):
        palavras_filtradas.append(palavra)

contador = Counter(palavras_filtradas)

quantidade_termos = st.selectbox(
    "Quantidade de termos no gráfico:",
    [10, 15, 20],
    index=1,
    key="mobilize_qtd_termos",
)

mais_frequentes = contador.most_common(
    quantidade_termos
)

if mais_frequentes:
    df_frequencia = pd.DataFrame(
        mais_frequentes,
        columns=["Termo", "Frequência"],
    )

    st.dataframe(df_frequencia)

    st.bar_chart(
        df_frequencia.set_index("Termo")
    )

    st.caption(
        "Frequência absoluta dos termos encontrados nos campos "
        "textuais coletados."
    )
else:
    st.warning(
        "Não há conteúdo textual suficiente para calcular a frequência."
    )
