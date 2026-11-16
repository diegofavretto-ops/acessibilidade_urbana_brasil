import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_ibge,
    inicializar_estado,
)


# =========================================================
# 1. DADOS
# =========================================================

inicializar_estado()

df = carregar_dados_ibge()


# =========================================================
# 2. CABEÇALHO
# =========================================================

st.title("Upload e Download")

st.write(
    "Utilize esta página para adicionar informações "
    "complementares à base do IBGE por meio de um arquivo "
    "CSV e depois baixar a base resultante."
)

st.info(
    "O arquivo complementar precisa possuir uma coluna "
    "chamada Estado. As demais colunas serão adicionadas "
    "à base principal utilizando essa coluna como referência."
)

st.divider()


# =========================================================
# 3. UPLOAD
# =========================================================

st.header(
    "1. Upload de dados complementares"
)


with st.container(
    border=True
):

    arquivo_enviado = st.file_uploader(
        "Selecione um arquivo CSV:",
        type=[
            "csv"
        ],
    )


    if arquivo_enviado is not None:

        try:

            dados_upload = pd.read_csv(
                arquivo_enviado
            )


            if "Estado" in (
                dados_upload.columns
            ):

                st.session_state[
                    "dados_upload"
                ] = dados_upload


                st.success(
                    "Arquivo carregado com sucesso."
                )


            else:

                st.error(
                    "O arquivo precisa possuir uma "
                    "coluna chamada Estado."
                )


        except Exception as erro:

            st.error(
                (
                    "Não foi possível ler o CSV: "
                    f"{erro}"
                )
            )


# =========================================================
# 4. RESUMO DO ARQUIVO ENVIADO
# =========================================================

dados_upload_estado = (
    st.session_state[
        "dados_upload"
    ]
)


if dados_upload_estado is not None:

    st.subheader(
        "Resumo do arquivo enviado"
    )


    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.metric(
            "Linhas",
            len(
                dados_upload_estado
            ),
        )


    with col2:

        st.metric(
            "Colunas",
            len(
                dados_upload_estado.columns
            ),
        )


    with col3:

        st.metric(
            "Estados informados",
            dados_upload_estado[
                "Estado"
            ].nunique(),
        )


    with st.expander(
        "Ver dados enviados"
    ):

        st.dataframe(
            dados_upload_estado,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# 5. BASE RESULTANTE
# =========================================================

st.divider()

st.header(
    "2. Base resultante"
)


df_complementado = df.copy()


if dados_upload_estado is not None:

    df_complementado = df.merge(
        dados_upload_estado,
        on="Estado",
        how="left",
    )


    st.success(
        "A base principal foi combinada com "
        "os dados complementares enviados."
    )


else:

    st.caption(
        "Nenhum arquivo complementar foi enviado. "
        "A base resultante corresponde à base original do IBGE."
    )


# =========================================================
# 6. RESUMO DA BASE
# =========================================================

col1, col2, col3 = st.columns(
    3
)


with col1:

    st.metric(
        "Linhas da base",
        len(
            df_complementado
        ),
    )


with col2:

    st.metric(
        "Colunas da base",
        len(
            df_complementado.columns
        ),
    )


with col3:

    st.metric(
        "Unidades da Federação",
        df_complementado[
            "Estado"
        ].nunique(),
    )


st.subheader(
    "Prévia da base"
)


st.dataframe(
    df_complementado.head(
        10
    ),
    use_container_width=True,
    hide_index=True,
)


with st.expander(
    "Ver base completa"
):

    st.dataframe(
        df_complementado,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 7. DOWNLOAD
# =========================================================

st.divider()

st.header(
    "3. Download"
)


st.write(
    "Baixe a base exibida acima em formato CSV."
)


csv_download = (
    df_complementado
    .to_csv(
        index=False
    )
    .encode(
        "utf-8-sig"
    )
)


st.download_button(
    label="Baixar dados em CSV",
    data=csv_download,
    file_name=(
        "dados_acessibilidade.csv"
    ),
    mime="text/csv",
    use_container_width=True,
)