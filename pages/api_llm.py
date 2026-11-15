import pandas as pd
import requests
import streamlit as st

from comum import carregar_dados_ibge


# =========================================================
# 1. DADOS PARA A INTERFACE
# =========================================================

df = carregar_dados_ibge()

estados = sorted(
    df["Estado"].unique()
)


# =========================================================
# 2. TÍTULO
# =========================================================

st.title("API e LLM local")

st.write(
    "Nesta página, o Streamlit consulta a FastAPI e utiliza "
    "o modelo local Qwen2.5-0.5B-Instruct para gerar um resumo "
    "dos indicadores de uma Unidade da Federação."
)


API_URL = st.text_input(
    "Endereço da API:",
    value="http://127.0.0.1:8000",
)


# =========================================================
# 3. STATUS DA API E DO MODELO
# =========================================================

st.header("1. Status da API e do modelo local")

if st.button(
    "Verificar API e modelo",
    key="verificar_api_modelo",
):

    try:

        resposta = requests.get(
            f"{API_URL}/ia/status",
            timeout=10,
        )

        if resposta.status_code == 200:

            status = resposta.json()

            st.success(
                "API e modelo local disponíveis."
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Modelo",
                    status["modelo"],
                )

            with col2:
                st.metric(
                    "Dispositivo",
                    status["dispositivo"].upper(),
                )

            with col3:
                st.metric(
                    "Arquivos locais",
                    (
                        "Sim"
                        if status["arquivos_locais"]
                        else "Não"
                    ),
                )

        else:

            st.error(
                f"A API respondeu com status "
                f"{resposta.status_code}."
            )

    except requests.RequestException:

        st.warning(
            "A API não está ativa. "
            "Em outro terminal execute: "
            "python -m uvicorn api:app"
        )


# =========================================================
# 4. CONSULTA DE INDICADORES PELA API
# =========================================================

st.header("2. Indicadores recebidos pela FastAPI")

estado_consulta = st.selectbox(
    "Selecione uma UF:",
    estados,
    key="estado_consulta_api",
)


if st.button(
    "Consultar indicadores",
    key="consultar_indicadores",
):

    try:

        resposta = requests.get(
            f"{API_URL}/ufs/{estado_consulta}",
            timeout=10,
        )

        if resposta.status_code == 200:

            dados = resposta.json()

            st.session_state[
                "dados_uf_api"
            ] = dados

            st.success(
                "Dados recebidos pela FastAPI."
            )

        elif resposta.status_code == 404:

            st.error(
                "A UF informada não foi encontrada."
            )

        else:

            st.error(
                f"Erro {resposta.status_code}: "
                f"{resposta.text}"
            )

    except requests.RequestException:

        st.warning(
            "Não foi possível conectar com a API."
        )


dados_api = st.session_state.get(
    "dados_uf_api"
)


if dados_api:

    st.subheader(
        f"Indicadores - {dados_api['Estado']}"
    )

    indicadores_api = {
        "Calçada/passeio":
            dados_api["Calcada_passeio_pct"],

        "Calçadas sem obstáculos":
            dados_api[
                "Calcadas_sem_obstaculos_pct"
            ],

        "Rampas":
            dados_api["Rampas_pct"],

        "Arborização":
            dados_api[
                "Arborizacao_com_arvores_pct"
            ],

        "Iluminação pública":
            dados_api[
                "Iluminacao_publica_pct"
            ],

        "Ponto ônibus/van":
            dados_api[
                "Ponto_onibus_van_pct"
            ],

        "Via para bicicleta":
            dados_api[
                "Via_bicicleta_pct"
            ],
    }


    df_indicadores_api = pd.DataFrame(
        [
            {
                "Indicador": indicador,
                "Percentual": percentual,
            }
            for indicador, percentual
            in indicadores_api.items()
        ]
    )


    st.dataframe(
        df_indicadores_api,
        use_container_width=True,
        hide_index=True,
    )


    st.bar_chart(
        df_indicadores_api.set_index(
            "Indicador"
        )
    )


    st.caption(
        "Os percentuais representam características "
        "observadas no entorno dos domicílios considerados "
        "na pesquisa do IBGE."
    )


# =========================================================
# 5. ANÁLISE COM O LLM LOCAL
# =========================================================

st.header("3. Resumo com IA local")

st.write(
    "A FastAPI envia os indicadores da UF selecionada "
    "ao modelo Qwen executado localmente. O modelo recebe "
    "instruções para utilizar somente os dados fornecidos."
)


estado_ia = st.selectbox(
    "Selecione a UF para gerar o resumo:",
    estados,
    key="estado_resumo_ia",
)


if st.button(
    "Gerar resumo com IA local",
    key="gerar_resumo_ia",
):

    try:

        with st.spinner(
            "Gerando resumo com o modelo local..."
        ):

            resposta = requests.post(
                f"{API_URL}/ia/resumo-uf",
                json={
                    "estado": estado_ia,
                },
                timeout=180,
            )


        if resposta.status_code == 200:

            st.session_state[
                "resultado_ia"
            ] = resposta.json()

            st.success(
                "Resumo gerado pelo modelo local."
            )

        elif resposta.status_code == 404:

            st.error(
                "A UF informada não foi encontrada."
            )

        elif resposta.status_code == 422:

            st.error(
                "Os dados enviados para a API "
                "não passaram pela validação."
            )

        elif resposta.status_code == 503:

            st.error(
                "O modelo local não está disponível "
                "ou não pôde ser executado."
            )

        else:

            st.error(
                f"Erro {resposta.status_code}: "
                f"{resposta.text}"
            )


    except requests.Timeout:

        st.error(
            "O modelo demorou mais do que o limite "
            "definido para gerar a resposta."
        )

    except requests.RequestException:

        st.warning(
            "Não foi possível conectar com a API."
        )


resultado_ia = st.session_state.get(
    "resultado_ia"
)


if resultado_ia:

    st.subheader(
        f"Resultado - {resultado_ia['estado']}"
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Região",
            resultado_ia["regiao"],
        )

    with col2:

        st.metric(
            "Modelo",
            resultado_ia["modelo"],
        )

    with col3:

        st.metric(
            "Execução",
            resultado_ia[
                "dispositivo"
            ].upper(),
        )


    nomes_indicadores = {
        "calcada_passeio_pct":
            "Calçada/passeio",

        "calcadas_sem_obstaculos_pct":
            "Calçadas sem obstáculos",

        "rampas_pct":
            "Rampas",

        "arborizacao_com_arvores_pct":
            "Arborização",
    }


    indicadores_ia = (
        resultado_ia["indicadores"]
    )


    df_indicadores_ia = pd.DataFrame(
        [
            {
                "Indicador":
                    nomes_indicadores[chave],

                "Percentual":
                    valor,
            }

            for chave, valor
            in indicadores_ia.items()
        ]
    )


    st.subheader(
        "Dados utilizados pelo modelo"
    )


    st.dataframe(
        df_indicadores_ia,
        use_container_width=True,
        hide_index=True,
    )


    st.bar_chart(
        df_indicadores_ia.set_index(
            "Indicador"
        )
    )


    st.subheader(
        "Resumo gerado pelo Qwen"
    )


    st.info(
        resultado_ia["resumo"]
    )


    st.caption(
        "O texto acima foi produzido pelo modelo "
        "Qwen2.5-0.5B-Instruct executado localmente. "
        "Os indicadores numéricos são provenientes "
        "da base do IBGE utilizada pelo projeto."
    )


# =========================================================
# 6. OBSERVAÇÃO COMPLEMENTAR
# =========================================================

st.header("4. Registrar observação pela API")

estado_observacao = st.selectbox(
    "UF da observação:",
    estados,
    key="estado_observacao_api",
)


texto_observacao = st.text_area(
    "Observação complementar:",
    placeholder=(
        "Ex.: informação complementar "
        "para teste da API."
    ),
)


if st.button(
    "Enviar observação",
    key="enviar_observacao_api",
):

    if not texto_observacao.strip():

        st.warning(
            "Digite uma observação antes de enviar."
        )

    else:

        try:

            resposta = requests.post(
                f"{API_URL}/observacoes",
                json={
                    "Estado":
                        estado_observacao,

                    "Observacao":
                        texto_observacao,
                },
                timeout=10,
            )


            if resposta.status_code == 200:

                st.success(
                    "Observação registrada "
                    "com sucesso pela API."
                )

            elif resposta.status_code == 422:

                st.error(
                    "A observação não passou "
                    "pela validação da API."
                )

            else:

                st.error(
                    f"Erro {resposta.status_code}: "
                    f"{resposta.text}"
                )


        except requests.RequestException:

            st.warning(
                "Não foi possível conectar "
                "com a API."
            )


# =========================================================
# 7. DOCUMENTAÇÃO
# =========================================================

st.divider()

st.caption(
    "A documentação automática da FastAPI fica disponível "
    "em http://127.0.0.1:8000/docs enquanto a API estiver ativa."
)