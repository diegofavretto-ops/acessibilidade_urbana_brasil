import pandas as pd
import streamlit as st

from comum import carregar_dados_ibge, indicadores


df = carregar_dados_ibge()
st.title("Comparações territoriais")
st.caption("Identifique diferenças entre estados e regiões | IBGE, Censo 2022")

aba1, aba2, aba3 = st.tabs(["UF e referências", "Duas UFs", "Regiões"])

with aba1:
    c1, c2 = st.columns(2)
    with c1:
        regioes = sorted(df["Regiao"].unique())
        regiao = st.selectbox("Região", regioes, index=regioes.index("Sul"), key="comparacao_regiao")
    recorte = df[df["Regiao"] == regiao]
    with c2:
        estados = sorted(recorte["Estado"])
        uf = st.selectbox("Unidade da Federação", estados, index=estados.index("Santa Catarina") if "Santa Catarina" in estados else 0, key="comparacao_estado")
    linha = recorte[recorte["Estado"] == uf].iloc[0]
    dados = pd.DataFrame([
        {"Indicador": nome, uf: linha[campo], "Média regional": recorte[campo].mean(), "Média das 27 UFs": df[campo].mean()}
        for nome, campo in indicadores.items()
    ])
    dados["Diferença regional (p.p.)"] = (dados[uf] - dados["Média regional"]).round(1)
    dados["Diferença UFs (p.p.)"] = (dados[uf] - dados["Média das 27 UFs"]).round(1)
    st.bar_chart(dados, x="Indicador", y=[uf, "Média regional", "Média das 27 UFs"], horizontal=True, stack=False, height=430)
    abaixo = dados[dados["Diferença regional (p.p.)"] < 0].sort_values("Diferença regional (p.p.)")
    acima = dados[dados["Diferença regional (p.p.)"] > 0].sort_values("Diferença regional (p.p.)", ascending=False)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Maior diferença abaixo da média regional**")
        if not abaixo.empty:
            item = abaixo.iloc[0]
            st.metric(item["Indicador"], f"{item['Diferença regional (p.p.)']:+.1f} p.p.")
        else:
            st.write("Nenhum indicador abaixo da média regional.")
    with c2:
        st.markdown("**Maior diferença acima da média regional**")
        if not acima.empty:
            item = acima.iloc[0]
            st.metric(item["Indicador"], f"{item['Diferença regional (p.p.)']:+.1f} p.p.")
        else:
            st.write("Nenhum indicador acima da média regional.")
    with st.expander("Valores e diferenças em pontos percentuais"):
        st.dataframe(dados.round(1), hide_index=True, use_container_width=True)

with aba2:
    estados = sorted(df["Estado"].unique())
    c1, c2 = st.columns(2)
    with c1:
        uf1 = st.selectbox("Primeira UF", estados, index=estados.index("Santa Catarina"), key="comparacao_uf1")
    with c2:
        alternativas = [uf for uf in estados if uf != uf1]
        uf2 = st.selectbox("Segunda UF", alternativas, index=alternativas.index("Paraná") if "Paraná" in alternativas else 0, key="comparacao_uf2")
    a = df.loc[df["Estado"] == uf1].iloc[0]
    b = df.loc[df["Estado"] == uf2].iloc[0]
    pares = pd.DataFrame([{"Indicador": nome, uf1: a[campo], uf2: b[campo], "Diferença (p.p.)": round(a[campo] - b[campo], 1)} for nome, campo in indicadores.items()])
    st.bar_chart(pares, x="Indicador", y=[uf1, uf2], horizontal=True, stack=False, height=410)
    maior = pares.loc[pares["Diferença (p.p.)"].abs().idxmax()]
    st.write(f"**Maior distância entre os valores:** {maior['Indicador']} ({abs(maior['Diferença (p.p.)']):.1f} p.p.).")
    st.caption(f"Diferença = {uf1} menos {uf2}; valor negativo indica percentual inferior na primeira UF.")
    st.dataframe(pares, hide_index=True, use_container_width=True)

with aba3:
    nome = st.selectbox("Indicador", list(indicadores), index=list(indicadores).index("Rampas"), key="comparacao_indicador_regiao")
    campo = indicadores[nome]
    medias = df.groupby("Regiao", as_index=False).agg(**{"Média (%)": (campo, "mean"), "Quantidade de UFs": ("Estado", "nunique")}).rename(columns={"Regiao": "Região"}).sort_values("Média (%)", ascending=False)
    maior, menor = medias.iloc[0], medias.iloc[-1]
    a, b, c = st.columns(3)
    a.metric(maior["Região"], f"{maior['Média (%)']:.1f}%")
    b.metric(menor["Região"], f"{menor['Média (%)']:.1f}%")
    c.metric("Amplitude regional", f"{maior['Média (%)'] - menor['Média (%)']:.1f} p.p.")
    st.bar_chart(medias, x="Região", y="Média (%)", horizontal=True, sort="-Média (%)", height=280)
    st.dataframe(medias.round(1), hide_index=True, use_container_width=True)

st.caption("Referências: médias simples dos percentuais estaduais, sem ponderação. Os indicadores têm denominadores próprios; as diferenças comparam o mesmo indicador. Fonte: IBGE/SIDRA 9584.")
