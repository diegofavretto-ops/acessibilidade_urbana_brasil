import pandas as pd
import streamlit as st

from comum import carregar_dados_ibge, indicadores, indicadores_principais


df = carregar_dados_ibge()


def percentual(valor):
    return f"{valor:.1f}%".replace(".", ",")


def pontos_percentuais(valor):
    if abs(valor) < 0.05:
        valor = 0.0
    return f"{valor:+.1f} p.p.".replace(".", ",")


# 1. Apresentação e abrangência do painel
st.title("Acessibilidade Urbana no Brasil")
st.caption("Censo Demográfico 2022 | Mobilidade de pedestres | ODS 11")
st.markdown(
    "Explore as condições do entorno dos domicílios brasileiros, "
    "compare estados e regiões e consulte informações sobre calçadas, "
    "rampas, circulação e ambiente urbano."
)

col1, col2, col3 = st.columns(3)
col1.metric("Unidades da Federação", df["Estado"].nunique())
col2.metric("Regiões brasileiras", df["Regiao"].nunique())
col3.metric("Indicadores do IBGE", len(indicadores))

# 2. Entrada para as principais análises
st.subheader("Explore os dados")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("**Panorama IBGE**")
        st.write("Consulte rankings e o perfil de cada UF.")
        st.page_link("pages/panorama.py", label="Ver indicadores")

with col2:
    with st.container(border=True):
        st.markdown("**Comparações territoriais**")
        st.write("Identifique diferenças entre estados e regiões.")
        st.page_link("pages/comparacoes.py", label="Comparar territórios")

with col3:
    with st.container(border=True):
        st.markdown("**Condições das calçadas**")
        st.write("Explore avaliações e textos do Mobilize Brasil.")
        st.page_link("pages/mobilize.py", label="Consultar levantamento")

# 3. Prévia analítica: visão nacional ou estadual
st.divider()
st.header("Visão geral dos indicadores")

opcao_nacional = "Brasil — média das UFs"
opcoes = [opcao_nacional] + sorted(df["Estado"].unique().tolist())
recorte = st.selectbox("Recorte territorial", opcoes, key="inicio_recorte")

campos = list(indicadores_principais.values())
medias_ufs = df[campos].mean()

if recorte == opcao_nacional:
    st.caption("Médias simples dos percentuais das UFs; não são percentuais nacionais ponderados.")
    for coluna, (nome, campo) in zip(st.columns(4), indicadores_principais.items()):
        coluna.metric(nome, percentual(medias_ufs[campo]))

    indicador = st.selectbox(
        "Indicador para comparar as regiões",
        list(indicadores_principais),
        index=list(indicadores_principais).index("Rampas"),
        key="inicio_indicador",
    )
    campo = indicadores_principais[indicador]
    medias_regioes = (
        df.groupby("Regiao", as_index=False)[campo]
        .mean()
        .rename(columns={"Regiao": "Região", campo: "Média das UFs (%)"})
        .sort_values("Média das UFs (%)", ascending=False)
    )
    grafico, destaques = st.columns([3, 2])
    with grafico:
        st.subheader(f"{indicador} por região")
        st.bar_chart(
            medias_regioes,
            x="Região",
            y="Média das UFs (%)",
            horizontal=True,
            sort="-Média das UFs (%)",
            height=260,
        )
    with destaques:
        st.subheader("Destaques")
        maior = df[campo].max()
        menor = df[campo].min()
        ufs_maior = ", ".join(df.loc[df[campo] == maior, "Estado"])
        ufs_menor = ", ".join(df.loc[df[campo] == menor, "Estado"])
        st.write(f"**Maior percentual:** {ufs_maior} ({percentual(maior)}).")
        st.write(f"**Menor percentual:** {ufs_menor} ({percentual(menor)}).")
        st.write(
            "**Diferença entre extremos:** "
            f"{pontos_percentuais(maior - menor).lstrip('+')}."
        )
        st.caption("Comparação descritiva entre as UFs da base.")

else:
    linha = df.loc[df["Estado"] == recorte].iloc[0]
    regiao = linha["Regiao"]
    medias_regiao = df.loc[df["Regiao"] == regiao, campos].mean()
    st.caption(f"{recorte} | Região {regiao} | Diferenças em relação à média simples regional")

    for coluna, (nome, campo) in zip(st.columns(4), indicadores_principais.items()):
        coluna.metric(
            nome,
            percentual(linha[campo]),
            delta=pontos_percentuais(linha[campo] - medias_regiao[campo]),
            delta_color="off",
        )

    comparacao = pd.DataFrame([
        {
            "Indicador": nome,
            recorte: float(linha[campo]),
            "Média regional": medias_regiao[campo],
            "Média das UFs": medias_ufs[campo],
        }
        for nome, campo in indicadores_principais.items()
    ])
    grafico, destaques = st.columns([3, 2])
    with grafico:
        st.subheader("Comparação com as médias")
        st.bar_chart(
            comparacao,
            x="Indicador",
            y=[recorte, "Média regional", "Média das UFs"],
            horizontal=True,
            stack=False,
            height=300,
        )
    with destaques:
        st.subheader("Destaques")
        diferencas = {
            nome: float(linha[campo] - medias_regiao[campo])
            for nome, campo in indicadores_principais.items()
        }
        abaixo = min(diferencas, key=diferencas.get)
        acima = max(diferencas, key=diferencas.get)
        if diferencas[abaixo] < -0.05:
            st.write(
                f"**Maior diferença abaixo da média regional:** {abaixo} "
                f"({pontos_percentuais(diferencas[abaixo])})."
            )
        else:
            st.write("Nenhum dos quatro indicadores está abaixo da média regional na precisão exibida.")
        if diferencas[acima] > 0.05:
            st.write(
                f"**Maior diferença acima da média regional:** {acima} "
                f"({pontos_percentuais(diferencas[acima])})."
            )
        else:
            st.write("Nenhum dos quatro indicadores está acima da média regional na precisão exibida.")
        posicao = int(df["Rampas_pct"].rank(ascending=False, method="min").loc[linha.name])
        st.write(f"**Rampas:** {posicao}ª posição entre {df['Estado'].nunique()} UFs (com empates).")

    with st.expander("Ver valores da comparação"):
        st.dataframe(comparacao.round(1), hide_index=True, use_container_width=True)

st.caption(
    "Os percentuais descrevem o entorno dos domicílios considerados pelo IBGE. "
    "Rampas e calçadas sem obstáculos têm como referência os entornos com calçada. "
    "As médias são simples entre UFs. As comparações não indicam conformidade normativa."
)

# 4. Recursos complementares e fontes
st.divider()
st.subheader("Recursos complementares")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/dados.py", label="Importar e exportar dados")
    st.caption("Consulte a base e adicione dados complementares em CSV.")
with col2:
    st.page_link("pages/api_llm.py", label="Análise com IA local")
    st.caption("Gere resumos dos indicadores e confira os dados utilizados.")

with st.expander("Sobre os dados e o projeto"):
    st.markdown(
        "**Fontes:** [IBGE — SIDRA, tabela 9584](https://sidra.ibge.gov.br/tabela/9584) "
        "e [Mobilize Brasil](https://www.mobilize.org.br/). "
        "Os levantamentos têm metodologias e abrangências diferentes."
    )
    st.write(
        "O painel apoia a consulta de informações sobre mobilidade e inclusão urbana, "
        "no contexto do ODS 11 e da dimensão Social do ESG. "
        "Não substitui diagnósticos técnicos locais."
    )
