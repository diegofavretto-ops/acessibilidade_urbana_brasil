import pandas as pd
import requests
import streamlit as st

from comum import carregar_dados_ibge


df = carregar_dados_ibge()
estados = sorted(df["Estado"].unique())
st.title("Análise complementar com IA")
st.caption("Consulte indicadores e solicite uma leitura textual com o Qwen local. As respostas podem conter imprecisões ou ser incompletas.")

with st.expander("Conexão e disponibilidade do modelo"):
    API_URL = st.text_input("Endereço da API:", value="http://127.0.0.1:8000").rstrip("/")
    if st.button("Verificar API e modelo", key="verificar_api_modelo", use_container_width=True):
        try:
            resposta = requests.get(f"{API_URL}/ia/status", timeout=10)
            if resposta.status_code == 200:
                st.session_state["status_ia"] = resposta.json()
            else:
                st.session_state.pop("status_ia", None)
                st.error(f"A API respondeu com status {resposta.status_code}.")
        except requests.RequestException:
            st.session_state.pop("status_ia", None)
            st.warning("Não foi possível conectar à API.")
    status_ia = st.session_state.get("status_ia")
    if status_ia:
        c1, c2, c3 = st.columns(3)
        c1.metric("Modelo", status_ia["modelo"])
        c2.metric("Execução", status_ia["dispositivo"].upper())
        c3.metric("Arquivos locais", "Sim" if status_ia["arquivos_locais"] else "Não")
        st.caption("Disponibilidade dos arquivos não garante que o modelo esteja carregado.")
    st.caption("Documentação: http://127.0.0.1:8000/docs | Inicialização: python -m uvicorn api:app")

aba_resumo, aba_consulta, aba_observacoes = st.tabs(["Resumo estadual", "Consulta de indicadores", "Observações"])

with aba_resumo:
    estado_ia = st.selectbox("Unidade da Federação", estados, index=estados.index("Santa Catarina"), key="estado_resumo_ia")
    if st.button("Gerar resumo com IA local", key="gerar_resumo_ia", use_container_width=True):
        try:
            with st.spinner("Gerando resumo com o modelo local..."):
                resposta = requests.post(f"{API_URL}/ia/resumo-uf", json={"estado": estado_ia}, timeout=180)
            if resposta.status_code == 200:
                st.session_state["resultado_ia"] = resposta.json()
                st.success("Resumo gerado pelo modelo local.")
            elif resposta.status_code == 404:
                st.error("A UF informada não foi encontrada.")
            elif resposta.status_code == 422:
                st.error("Os dados enviados não passaram pela validação da API.")
            elif resposta.status_code == 503:
                st.error("O modelo local não está disponível ou não pôde ser executado.")
            else:
                st.error(f"Erro {resposta.status_code}: {resposta.text}")
        except requests.Timeout:
            st.error("O modelo demorou mais do que o limite definido para gerar a resposta.")
        except requests.RequestException:
            st.warning("Não foi possível conectar com a API.")
    resultado_ia = st.session_state.get("resultado_ia")
    if resultado_ia:
        st.subheader(f"Resultado — {resultado_ia['estado']}")
        nomes_indicadores = {"calcada_passeio_pct": "Calçada/passeio", "calcadas_sem_obstaculos_pct": "Calçadas sem obstáculos", "rampas_pct": "Rampas", "arborizacao_com_arvores_pct": "Arborização"}
        df_indicadores = pd.DataFrame([{"Indicador": nomes_indicadores.get(chave, chave), "Percentual (%)": valor} for chave, valor in resultado_ia["indicadores"].items()])
        for coluna, (_, item) in zip(st.columns(4), df_indicadores.iterrows()):
            coluna.metric(item["Indicador"], f"{item['Percentual (%)']:.1f}%")
        st.bar_chart(df_indicadores, x="Indicador", y="Percentual (%)", horizontal=True, height=240)
        st.markdown("**Resumo gerado pelo Qwen**")
        st.write(resultado_ia["resumo"])
        st.caption(f"Região: {resultado_ia['regiao']} | Modelo: {resultado_ia['modelo']} | Execução: {resultado_ia['dispositivo'].upper()}")
        with st.expander("Ver dados enviados ao modelo"):
            st.dataframe(df_indicadores, hide_index=True, use_container_width=True)
        st.caption("Confronte o texto gerado com os valores apresentados. Fonte dos indicadores: IBGE/SIDRA 9584.")

with aba_consulta:
    estado_consulta = st.selectbox("Unidade da Federação", estados, key="estado_consulta_api")
    if st.button("Consultar indicadores", key="consultar_indicadores", use_container_width=True):
        try:
            resposta = requests.get(f"{API_URL}/ufs/{estado_consulta}", timeout=10)
            if resposta.status_code == 200:
                st.session_state["dados_uf_api"] = resposta.json()
            elif resposta.status_code == 404:
                st.error("A UF informada não foi encontrada.")
            else:
                st.error(f"Erro {resposta.status_code}: {resposta.text}")
        except requests.RequestException:
            st.warning("Não foi possível conectar com a API.")
    dados_api = st.session_state.get("dados_uf_api")
    if dados_api:
        st.subheader(f"Indicadores — {dados_api['Estado']}")
        indicadores_api = {"Calçada/passeio": dados_api["Calcada_passeio_pct"], "Calçadas sem obstáculos": dados_api["Calcadas_sem_obstaculos_pct"], "Rampas": dados_api["Rampas_pct"], "Arborização": dados_api["Arborizacao_com_arvores_pct"], "Iluminação pública": dados_api["Iluminacao_publica_pct"], "Ponto ônibus/van": dados_api["Ponto_onibus_van_pct"], "Via para bicicleta": dados_api["Via_bicicleta_pct"]}
        for coluna, (nome, valor) in zip(st.columns(4), indicadores_api.items()):
            coluna.metric(nome, f"{valor:.1f}%")
        df_api = pd.DataFrame([{"Indicador": nome, "Percentual (%)": valor} for nome, valor in indicadores_api.items()])
        st.bar_chart(df_api, x="Indicador", y="Percentual (%)", horizontal=True, height=350)
        with st.expander("Ver indicadores em tabela"):
            st.dataframe(df_api, hide_index=True, use_container_width=True)

with aba_observacoes:
    estado_observacao = st.selectbox("UF da observação", estados, key="estado_observacao_api")
    texto_observacao = st.text_area("Observação complementar", max_chars=500)
    if st.button("Enviar observação", key="enviar_observacao_api", use_container_width=True):
        if not texto_observacao.strip():
            st.warning("Digite uma observação antes de enviar.")
        else:
            try:
                resposta = requests.post(f"{API_URL}/observacoes", json={"Estado": estado_observacao, "Observacao": texto_observacao}, timeout=10)
                if resposta.status_code == 200:
                    st.success("Observação registrada com sucesso.")
                elif resposta.status_code == 422:
                    st.error("A observação não passou pela validação da API.")
                else:
                    st.error(f"Erro {resposta.status_code}: {resposta.text}")
            except requests.RequestException:
                st.warning("Não foi possível conectar com a API.")

st.caption("Os percentuais se referem às características do entorno dos domicílios considerados. A IA é um recurso complementar, não uma avaliação técnica.")
