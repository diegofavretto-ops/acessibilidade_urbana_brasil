import streamlit as st

from comum import inicializar_estado


st.set_page_config(
    page_title="Acessibilidade Urbana no Brasil",
    page_icon="🚶",
    layout="wide",
)


inicializar_estado()


paginas = {
    "Projeto": [
        st.Page(
            "pages/inicio.py",
            title="Início",
            icon="🏠",
            default=True,
        ),
    ],
    "Análises": [
        st.Page(
            "pages/panorama.py",
            title="Panorama IBGE",
            icon="📊",
        ),
        st.Page(
            "pages/comparacoes.py",
            title="Comparações",
            icon="🔎",
        ),
        st.Page(
            "pages/mobilize.py",
            title="Referências Web",
            icon="🚶",
        ),
    ],
    "Dados e integração": [
        st.Page(
            "pages/dados.py",
            title="Upload e Download",
            icon="📁",
        ),
        st.Page(
            "pages/api_llm.py",
            title="API e LLM",
            icon="🤖",
        ),
    ],
}


pagina = st.navigation(paginas)
pagina.run()


st.caption(
    "Projeto relacionado ao ODS 11 - Cidades e Comunidades Sustentáveis."
)