import pandas as pd
import streamlit as st

from comum import carregar_dados_ibge, indicadores


df = carregar_dados_ibge()
st.title("Panorama IBGE")
st.caption("Censo 2022 | Comparação dos indicadores do entorno dos domicílios")

aba_ranking, aba_perfil = st.tabs(["Ranking de UFs", "Perfil estadual"])
with aba_ranking:
    col1, col2 = st.columns(2)
    with col1:
        nome = st.selectbox("Indicador", list(indicadores), index=list(indicadores).index("Rampas"))
    with col2:
        regiao = st.selectbox("Recorte geográfico", ["Todas as regiões"] + sorted(df["Regiao"].unique()))
    campo = indicadores[nome]
    recorte = df if regiao == "Todas as regiões" else df[df["Regiao"] == regiao]
    ranking = recorte[["Estado", "Regiao", campo]].rename(columns={"Regiao": "Região", campo: "Percentual (%)"}).sort_values("Percentual (%)", ascending=False).reset_index(drop=True)
    ranking.insert(0, "Posição", ranking["Percentual (%)"].rank(ascending=False, method="min").astype(int))
    maior, menor = ranking.iloc[0], ranking.iloc[-1]
    media = ranking["Percentual (%)"].mean()
    a, b, c, d = st.columns(4)
    a.metric("Maior percentual", f"{maior['Percentual (%)']:.1f}%", help=maior["Estado"])
    a.caption(maior["Estado"])
    b.metric("Média das UFs", f"{media:.1f}%")
    c.metric("Menor percentual", f"{menor['Percentual (%)']:.1f}%")
    c.caption(menor["Estado"])
    d.metric("Amplitude", f"{maior['Percentual (%)'] - menor['Percentual (%)']:.1f} p.p.")
    st.subheader(f"{nome} — {regiao}")
    st.bar_chart(ranking, x="Estado", y="Percentual (%)", horizontal=True, sort="-Percentual (%)", height=max(260, len(ranking) * 28 + 50))
    abaixo = int((ranking["Percentual (%)"] < media).sum())
    st.write(f"**Leitura do indicador:** {abaixo} de {len(ranking)} UFs do recorte estão abaixo da média simples. A diferença entre o maior e o menor valor é de {maior['Percentual (%)'] - menor['Percentual (%)']:.1f} p.p.")
    esquerda, direita = st.columns(2)
    with esquerda:
        st.markdown("**Cinco maiores percentuais**")
        st.dataframe(ranking.head(5), hide_index=True, use_container_width=True)
    with direita:
        st.markdown("**Cinco menores percentuais**")
        st.dataframe(ranking.sort_values("Percentual (%)").head(5), hide_index=True, use_container_width=True)
    with st.expander("Ranking completo"):
        st.dataframe(ranking, hide_index=True, use_container_width=True)
        st.download_button("Exportar ranking (CSV)", ranking.to_csv(index=False).encode("utf-8-sig"), "ranking_ibge.csv", "text/csv")

with aba_perfil:
    col1, col2 = st.columns(2)
    with col1:
        reg = st.selectbox("Região", sorted(df["Regiao"].unique()), key="panorama_regiao")
    with col2:
        uf = st.selectbox("Unidade da Federação", sorted(df.loc[df["Regiao"] == reg, "Estado"]), key="panorama_estado")
    linha = df.loc[df["Estado"] == uf].iloc[0]
    perfil = pd.DataFrame([
        {"Indicador": nome, "Percentual (%)": linha[campo], "Posição entre as UFs": int(df[campo].rank(method="min", ascending=False).loc[linha.name])}
        for nome, campo in indicadores.items()
    ])
    st.subheader(uf)
    for coluna, (_, item) in zip(st.columns(4), perfil[perfil["Indicador"].isin(["Calçada/passeio", "Calçadas sem obstáculos", "Rampas", "Arborização"])].iterrows()):
        with coluna:
            st.metric(item["Indicador"], f"{item['Percentual (%)']:.1f}%")
            st.caption(f"{item['Posição entre as UFs']}ª posição entre as UFs")
    st.bar_chart(perfil, x="Indicador", y="Percentual (%)", horizontal=True, height=330)
    st.dataframe(perfil, hide_index=True, use_container_width=True)

st.caption("Médias simples das UFs; não correspondem a um percentual nacional ponderado. Rampas e calçadas sem obstáculos referem-se aos entornos com calçada. Fonte: IBGE/SIDRA 9584.")
