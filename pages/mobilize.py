from collections import Counter
import re

import pandas as pd
import requests
import streamlit as st

from comum import carregar_dados_mobilize, carregar_mobilize_panorama


df_mobilize = carregar_dados_mobilize()
df_panorama = carregar_mobilize_panorama()

st.title("Condições das calçadas — Mobilize")
st.caption("Campanha Calçadas do Brasil | Levantamento complementar, não diretamente comparável aos percentuais do IBGE.")

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

categorias_panorama = (df_panorama["Categorias"].str.split("; ").explode().dropna().drop_duplicates().sort_values().tolist())

aba_notas, aba_textos, aba_ia = st.tabs(["Avaliações das calçadas", "Panorama textual", "Síntese com IA local"])

with aba_notas:
    c1, c2 = st.columns(2)
    with c1:
        criterio_nome = st.selectbox("Critério de avaliação", list(criterios_mobilize), index=list(criterios_mobilize).index("Nota média geral"), key="mobilize_criterio")
    with c2:
        localidades = sorted(df_mobilize["Cidade"].dropna().astype(str).unique())
        localidade = st.selectbox("Cidade/localidade (como registrada na fonte)", ["Todas"] + localidades)
    recorte = df_mobilize if localidade == "Todas" else df_mobilize[df_mobilize["Cidade"].astype(str) == localidade]
    criterio = criterios_mobilize[criterio_nome]
    ranking = recorte[["Endereco", "Cidade", criterio]].copy()
    ranking[criterio] = pd.to_numeric(ranking[criterio], errors="coerce")
    ranking = ranking.dropna(subset=[criterio]).rename(columns={"Endereco": "Endereço", "Cidade": "Cidade/localidade", criterio: "Nota (0 a 10)"})

    if not ranking.empty:
        notas = ranking["Nota (0 a 10)"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nota média", f"{notas.mean():.2f} / 10")
        c2.metric("Locais com nota válida", len(ranking))
        c3.metric("Menor nota", f"{notas.min():.2f}")
        c4.metric("Maior nota", f"{notas.max():.2f}")
        st.write(f"**Amplitude das avaliações:** {notas.max() - notas.min():.2f} pontos no critério selecionado. As notas descrevem os locais observados, não toda a cidade ou todo o país.")
        if criterio == "Irregularidades":
            st.caption("A nota avalia as condições do piso; não é uma contagem de irregularidades.")
        st.subheader("Locais em destaque")
        esquerda, direita = st.columns(2)
        with esquerda:
            st.markdown("**Cinco maiores notas**")
            st.dataframe(ranking.nlargest(5, "Nota (0 a 10)"), hide_index=True, use_container_width=True)
        with direita:
            st.markdown("**Cinco menores notas**")
            st.dataframe(ranking.nsmallest(5, "Nota (0 a 10)"), hide_index=True, use_container_width=True)
        with st.expander("Consultar todas as avaliações do recorte"):
            st.dataframe(recorte, hide_index=True, use_container_width=True)
            st.download_button("Exportar avaliações (CSV)", recorte.to_csv(index=False).encode("utf-8-sig"), "avaliacoes_mobilize.csv", "text/csv")
    else:
        st.info("Não há notas válidas para o critério nesse recorte.")

    st.subheader("Desempenho por critério")
    df_medias = pd.DataFrame([
        {"Critério": nome, "Nota média": pd.to_numeric(recorte[campo], errors="coerce").mean(), "Avaliações válidas": pd.to_numeric(recorte[campo], errors="coerce").count()}
        for nome, campo in criterios_mobilize.items() if campo != "Media"
    ]).dropna(subset=["Nota média"]).sort_values("Nota média", ascending=False)
    if not df_medias.empty:
        st.bar_chart(df_medias, x="Critério", y="Nota média", horizontal=True, sort="-Nota média", height=380)
        menor = df_medias.iloc[-1]
        maior = df_medias.iloc[0]
        st.write(f"**Menor média do recorte:** {menor['Critério']} ({menor['Nota média']:.2f}/10). **Maior média:** {maior['Critério']} ({maior['Nota média']:.2f}/10).")
        with st.expander("Ver valores e quantidade de avaliações"):
            st.dataframe(df_medias.round(2), hide_index=True, use_container_width=True)
    st.caption("As médias utilizam somente notas válidas de cada critério. A quantidade de avaliações pode variar entre critérios.")

with aba_textos:
    st.subheader("Temas identificados nos textos")
    categoria_escolhida = st.selectbox("Categoria", ["Todas"] + categorias_panorama, key="mobilize_panorama_categoria")
    if categoria_escolhida == "Todas":
        df_filtrado = df_panorama.copy()
    else:
        df_filtrado = df_panorama[df_panorama["Categorias"].fillna("").str.split("; ").apply(lambda categorias: categoria_escolhida in categorias)]
    col1, col2 = st.columns(2)
    col1.metric("Trechos do recorte", len(df_filtrado))
    col2.metric("Total de trechos coletados", len(df_panorama))
    texto_panorama = " ".join(df_filtrado["Texto"].fillna("").astype(str).tolist())
    palavras = re.findall(r"[A-Za-zÀ-ÿ]+", texto_panorama.lower())
    palavras_excluidas = set("aos ainda alguma algumas alguns assim cada com como contra das deve devem dos ela elas ele eles entre essa essas esse esses esta estas este estes foram mais mesmo muito muitos muita muitas nas não nos onde outra outras outro outros para pela pelas pelo pelos pode podem pois por quando que são sem sendo ser seu seus sua suas sobre também tem ter uma umas uns".split())
    contador = Counter(palavra for palavra in palavras if len(palavra) >= 4 and palavra not in palavras_excluidas)
    esquerda, direita = st.columns(2)
    with esquerda:
        st.markdown("**Categorias mais mencionadas no conjunto coletado**")
        frequencia_categorias = df_panorama["Categorias"].str.split("; ").explode().value_counts().rename_axis("Categoria").reset_index(name="Frequência")
        if not frequencia_categorias.empty:
            st.bar_chart(frequencia_categorias, x="Categoria", y="Frequência", horizontal=True, sort="-Frequência", height=360)
            with st.expander("Ver frequências das categorias"):
                st.dataframe(frequencia_categorias, hide_index=True, use_container_width=True)
        st.caption("Um trecho pode mencionar várias categorias.")
    with direita:
        st.markdown("**Termos recorrentes no recorte**")
        quantidade_termos = st.selectbox("Quantidade de termos", [10, 15, 20], key="mobilize_qtd_termos")
        df_frequencia = pd.DataFrame(contador.most_common(quantidade_termos), columns=["Termo", "Frequência"])
        if not df_frequencia.empty:
            st.bar_chart(df_frequencia, x="Termo", y="Frequência", horizontal=True, sort="-Frequência", height=360)
            with st.expander("Ver frequências dos termos"):
                st.dataframe(df_frequencia, hide_index=True, use_container_width=True)
        else:
            st.info("Sem termos suficientes no recorte.")
        st.caption("Frequência de palavras não equivale à frequência de problemas constatados.")
    st.subheader("Textos originais")
    st.dataframe(df_filtrado[["Categorias", "Texto"]], hide_index=True, use_container_width=True)

# A geração de IA continua usando a mesma rota, parâmetros, modelo e tratamento
# de contingência. Apenas a organização da interface foi ajustada.
with aba_ia:
    st.subheader("Sumarização dos textos com IA local")
    st.caption("O resultado é complementar. A verificação automática por expressões não garante fidelidade semântica.")
    with st.expander("Configuração da API"):
        api_url = st.text_input("Endereço da API:", value="http://127.0.0.1:8000", key="mobilize_api_url")

    if not categorias_panorama:
        st.info("Não há categorias disponíveis para sumarização.")
    else:
        categoria_ia = st.selectbox("Selecione uma categoria para gerar a síntese:", categorias_panorama, key="mobilize_categoria_ia")
        trechos_categoria = df_panorama[df_panorama["Categorias"].str.contains(categoria_ia, regex=False, na=False)]
        col1, col2 = st.columns(2)
        col1.metric("Categoria selecionada", categoria_ia)
        col2.metric("Trechos disponíveis", len(trechos_categoria))
        with st.expander("Ver textos que serão enviados ao modelo"):
            st.dataframe(trechos_categoria[["Categorias", "Texto"]], use_container_width=True, hide_index=True)
        if st.button("Gerar síntese com IA local", key="mobilize_gerar_sintese", use_container_width=True):
            try:
                with st.spinner("O modelo local está analisando os textos..."):
                    resposta = requests.post(f"{api_url}/ia/resumo-mobilize", json={"categoria": categoria_ia}, timeout=180)
                if resposta.status_code == 200:
                    st.session_state["mobilize_resumo_ia"] = resposta.json()
                elif resposta.status_code == 404:
                    st.error("A categoria selecionada não foi encontrada nos dados.")
                elif resposta.status_code == 422:
                    st.error("Os dados enviados não passaram pela validação da API.")
                elif resposta.status_code == 503:
                    st.error("O modelo local ou os dados necessários não estão disponíveis.")
                else:
                    st.error(f"A API retornou o erro {resposta.status_code}.")
            except requests.Timeout:
                st.error("O modelo demorou mais do que o tempo limite para responder.")
            except requests.RequestException:
                st.warning("Não foi possível conectar com a FastAPI. Verifique se ela está sendo executada em http://127.0.0.1:8000.")

        resultado_ia = st.session_state.get("mobilize_resumo_ia")
        if resultado_ia:
            # Identifique o recorte do resultado sem alterar a resposta da API.
            st.caption(f"Resultado da última solicitação: {resultado_ia.get('categoria', 'Não informada')}")
            metodo_resumo = resultado_ia.get("metodo_resumo", "Método não informado")
            if metodo_resumo == "Resumo de segurança baseado nas evidências":
                st.warning("O resultado abaixo é uma saída alternativa, não uma síntese produzida pelo LLM.")
            elif metodo_resumo == "LLM - resposta corrigida":
                st.info("O modelo realizou uma segunda tentativa aceita pela verificação de expressões. Confira os textos originais.")
            else:
                st.info("Resposta do modelo. A verificação automática não elimina possíveis extrapolações.")
            st.subheader("Síntese gerada")
            col1, col2, col3 = st.columns(3)
            col1.metric("Trechos utilizados", resultado_ia["quantidade_trechos"])
            col2.metric("Modelo", resultado_ia["modelo"])
            col3.metric("Execução", resultado_ia["dispositivo"].upper())
            st.caption(f"Método da síntese: {metodo_resumo}")
            st.write(resultado_ia["resumo"])
            with st.expander("Ver evidências textuais utilizadas"):
                for indice, trecho in enumerate(resultado_ia["trechos"], start=1):
                    st.markdown(f"**Trecho {indice}**")
                    st.write(trecho)
            st.caption("A síntese deve ser interpretada juntamente com os textos originais.")

st.caption("Fonte: Mobilize Brasil — Calçadas do Brasil e Panorama das Calçadas.")
