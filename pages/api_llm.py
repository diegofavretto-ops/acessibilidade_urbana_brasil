import requests
import streamlit as st

from comum import carregar_dados_ibge


df = carregar_dados_ibge()


st.title("API e preparação para LLM")

st.write(
    "O Streamlit é a interface usada pelas pessoas. A FastAPI cria "
    "endpoints que podem ser consumidos por outros programas."
)


API_URL = st.text_input(
    "Endereço da API:",
    value="http://127.0.0.1:8000",
)


st.header("1. Testar a API")

if st.button("Verificar API"):
    try:
        resposta = requests.get(
            f"{API_URL}/",
            timeout=5,
        )

        if resposta.status_code == 200:
            st.success("API funcionando.")
            st.json(resposta.json())
        else:
            st.error(
                f"A API respondeu com status {resposta.status_code}."
            )

    except requests.RequestException:
        st.warning(
            "A API não está ativa. Em outro terminal execute: "
            "uvicorn api:app --reload"
        )


st.header("2. Consulta GET")

estado = st.selectbox(
    "UF para consultar pela API:",
    sorted(df["Estado"].unique()),
    key="api_estado_get",
)

if st.button("Consultar UF"):
    try:
        resposta = requests.get(
            f"{API_URL}/ufs/{estado}",
            timeout=5,
        )

        if resposta.status_code == 200:
            st.success(
                "Dados recebidos da FastAPI."
            )
            st.json(resposta.json())
        else:
            st.error(
                f"Erro {resposta.status_code}: {resposta.text}"
            )

    except requests.RequestException:
        st.warning(
            "Não foi possível conectar com a API."
        )


st.header("3. Envio POST")

estado_post = st.selectbox(
    "UF da observação:",
    sorted(df["Estado"].unique()),
    key="api_estado_post",
)

texto_observacao = st.text_area(
    "Observação complementar:",
    placeholder="Ex.: informação complementar para teste da API.",
)

if st.button("Enviar observação"):
    if not texto_observacao.strip():
        st.warning("Digite uma observação antes de enviar.")
    else:
        try:
            resposta = requests.post(
                f"{API_URL}/observacoes",
                json={
                    "Estado": estado_post,
                    "Observacao": texto_observacao,
                },
                timeout=5,
            )

            if resposta.status_code == 200:
                st.success(
                    "Observação enviada pela API."
                )
                st.json(resposta.json())
            else:
                st.error(
                    f"Erro {resposta.status_code}: {resposta.text}"
                )

        except requests.RequestException:
            st.warning(
                "Não foi possível conectar com a API."
            )


st.header("4. Preparação para LLM")

st.write(
    "O TP3 ainda não implementa um modelo de linguagem. Nesta etapa "
    "o projeto apenas prepara os dados e a API para a próxima fase."
)

st.subheader("Aplicações futuras selecionadas")

st.write(
    "**Perguntas e respostas (Q&A):** permitir perguntas como "
    "'qual UF possui maior percentual de rampas?' ou 'como Santa "
    "Catarina se compara à Região Sul?'."
)

st.write(
    "**Geração de relatórios:** transformar os indicadores numéricos "
    "em resumos textuais automáticos sobre uma UF ou região."
)

st.info(
    "Classificação de sentimentos não foi priorizada porque as "
    "principais fontes do projeto são dados estatísticos e técnicos, "
    "e não opiniões de usuários."
)

st.caption(
    "A documentação automática da FastAPI fica disponível em "
    "http://127.0.0.1:8000/docs quando a API está em execução."
)
