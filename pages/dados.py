import pandas as pd
import streamlit as st

from comum import (
    carregar_dados_ibge,
    inicializar_estado,
)


inicializar_estado()
df = carregar_dados_ibge()


st.title("Upload e Download")

st.write(
    "Nesta página é possível complementar a base do IBGE com um "
    "arquivo CSV próprio e baixar o resultado."
)


st.header("1. Upload de dados complementares")

st.write(
    "O CSV precisa possuir uma coluna chamada Estado. As demais "
    "colunas serão acrescentadas à base principal por meio de um merge."
)

arquivo_enviado = st.file_uploader(
    "Selecione um arquivo CSV:",
    type=["csv"],
)

if arquivo_enviado is not None:
    try:
        dados_upload = pd.read_csv(
            arquivo_enviado
        )

        if "Estado" in dados_upload.columns:
            st.session_state[
                "dados_upload"
            ] = dados_upload

            st.success(
                "Arquivo carregado com sucesso."
            )
        else:
            st.error(
                "O arquivo precisa possuir uma coluna chamada Estado."
            )

    except Exception as erro:
        st.error(
            f"Não foi possível ler o CSV: {erro}"
        )


st.header("2. Base resultante")

df_complementado = df.copy()

if st.session_state["dados_upload"] is not None:
    st.subheader("Dados enviados")
    st.dataframe(
        st.session_state["dados_upload"]
    )

    df_complementado = df.merge(
        st.session_state["dados_upload"],
        on="Estado",
        how="left",
    )

    st.subheader("Base complementada")
else:
    st.caption(
        "Nenhum arquivo complementar foi enviado; a base abaixo é a base original."
    )

st.dataframe(df_complementado)


st.header("3. Download")

csv_download = (
    df_complementado
    .to_csv(index=False)
    .encode("utf-8-sig")
)

st.download_button(
    label="Baixar dados em CSV",
    data=csv_download,
    file_name="dados_acessibilidade.csv",
    mime="text/csv",
)
