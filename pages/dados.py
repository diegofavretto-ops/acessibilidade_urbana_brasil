import pandas as pd
import streamlit as st

from comum import carregar_dados_ibge, inicializar_estado


inicializar_estado()
df = carregar_dados_ibge()
st.title("Dados e exportação")
st.caption("Consulte, complemente e exporte a base estadual de indicadores.")

with st.expander("Adicionar dados complementares (CSV)"):
    st.caption("A coluna Estado deve conter os nomes das UFs, uma linha por UF. Utilize nomes de colunas diferentes dos indicadores originais.")
    if "chave_upload_dados" not in st.session_state:
        st.session_state["chave_upload_dados"] = 0
    if st.button("Remover dados complementares"):
        st.session_state["dados_upload"] = None
        st.session_state["chave_upload_dados"] += 1
    arquivo = st.file_uploader("Arquivo CSV", type=["csv"], key=f"upload_complementar_{st.session_state['chave_upload_dados']}")
    if arquivo is not None:
        try:
            dados = pd.read_csv(arquivo)
            if "Estado" not in dados.columns:
                raise ValueError("A coluna Estado é obrigatória.")
            dados["Estado"] = dados["Estado"].astype("string").str.strip()
            if dados["Estado"].isna().any() or dados["Estado"].duplicated().any():
                raise ValueError("Informe uma única linha por UF, sem valores vazios.")
            desconhecidos = sorted(set(dados["Estado"]) - set(df["Estado"]))
            if desconhecidos:
                raise ValueError("UFs não reconhecidas: " + ", ".join(desconhecidos))
            comuns = (set(dados.columns) & set(df.columns)) - {"Estado"}
            if comuns:
                raise ValueError("Renomeie as colunas complementares já existentes: " + ", ".join(sorted(comuns)))
            st.session_state["dados_upload"] = dados
            st.success("Dados complementares disponíveis.")
        except Exception as erro:
            st.error(f"Não foi possível utilizar o arquivo: {erro}")
            st.session_state["dados_upload"] = None

upload = st.session_state["dados_upload"]
base = df.copy() if upload is None else df.merge(upload, on="Estado", how="left", validate="one_to_one")
col1, col2, col3 = st.columns(3)
col1.metric("Unidades da Federação", base["Estado"].nunique())
col2.metric("Colunas da base", len(base.columns))
col3.metric("UFs complementadas", 0 if upload is None else upload["Estado"].nunique())
if upload is not None:
    with st.expander("Ver arquivo complementar"):
        st.dataframe(upload, hide_index=True, use_container_width=True)
regiao = st.selectbox("Região", ["Todas"] + sorted(base["Regiao"].unique()))
exibicao = base if regiao == "Todas" else base[base["Regiao"] == regiao]
st.subheader("Base de indicadores")
st.dataframe(exibicao, hide_index=True, use_container_width=True)
st.download_button("Exportar recorte em CSV", exibicao.to_csv(index=False).encode("utf-8-sig"), "dados_acessibilidade.csv", "text/csv", use_container_width=True)
st.caption("Fonte principal: IBGE, Censo Demográfico 2022. Dados complementares são fornecidos pelo usuário.")
