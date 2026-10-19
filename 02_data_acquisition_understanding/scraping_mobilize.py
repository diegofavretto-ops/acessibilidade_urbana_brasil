import csv
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. FONTE
# =========================================================

url = (
    "https://www.mobilize.org.br/"
    "estatisticas/31/"
    "calcadas-do-brasil-ficam-com-media-34.html"
)


# =========================================================
# 2. ACESSO À PÁGINA
# =========================================================

resposta = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30,
)

print("Status da página:", resposta.status_code)

resposta.raise_for_status()
resposta.encoding = resposta.apparent_encoding


# =========================================================
# 3. BEAUTIFULSOUP
# =========================================================

soup = BeautifulSoup(
    resposta.text,
    "html.parser",
)


tabelas = soup.find_all("table")
tabela_dados = None

for tabela in tabelas:
    texto_tabela = tabela.get_text(
        " ",
        strip=True,
    )

    if (
        "Endereço" in texto_tabela
        and "Rampas" in texto_tabela
        and "Arborização" in texto_tabela
    ):
        tabela_dados = tabela
        break


if tabela_dados is None:
    raise ValueError(
        "A tabela esperada não foi encontrada na página."
    )


# =========================================================
# 4. EXTRAÇÃO DAS LINHAS
# =========================================================

dados = []

for linha in tabela_dados.find_all("tr"):
    celulas = linha.find_all("td")

    valores = []

    for celula in celulas:
        texto = celula.get_text(
            " ",
            strip=True,
        )
        valores.append(texto)

    # A tabela possui uma primeira coluna que não será usada.
    if len(valores) == 12:
        valores = valores[1:]

    if (
        len(valores) == 11
        and valores[0].strip()
        and valores[-1].strip()
    ):
        dados.append(valores)


colunas = [
    "Endereco",
    "Irregularidades",
    "Degraus",
    "Inclinacao",
    "Largura",
    "Rampas",
    "Obstaculos",
    "Iluminacao",
    "Arborizacao",
    "Sinalizacao",
    "Media",
]


df_mobilize = pd.DataFrame(
    dados,
    columns=colunas,
)


# =========================================================
# 5. SEPARAÇÃO DE CIDADE/LOCALIDADE
# =========================================================

def separar_cidade(texto):
    texto = str(texto).strip()

    posicao_virgula = texto.rfind(",")
    posicao_traco = texto.rfind(" - ")

    if posicao_virgula > posicao_traco:
        endereco = texto[:posicao_virgula].strip()
        cidade = texto[posicao_virgula + 1:].strip()

    elif posicao_traco != -1:
        endereco = texto[:posicao_traco].strip()
        cidade = texto[posicao_traco + 3:].strip()

    else:
        endereco = texto
        cidade = ""

    return pd.Series([endereco, cidade])


if not df_mobilize.empty:
    df_mobilize[["Endereco", "Cidade"]] = (
        df_mobilize["Endereco"].apply(separar_cidade)
    )


df_mobilize = df_mobilize[
    [
        "Endereco",
        "Cidade",
        "Irregularidades",
        "Degraus",
        "Inclinacao",
        "Largura",
        "Rampas",
        "Obstaculos",
        "Iluminacao",
        "Arborizacao",
        "Sinalizacao",
        "Media",
    ]
]


# =========================================================
# 6. CONVERSÃO PARA NÚMEROS
# =========================================================

colunas_numericas = [
    "Irregularidades",
    "Degraus",
    "Inclinacao",
    "Largura",
    "Rampas",
    "Obstaculos",
    "Iluminacao",
    "Arborizacao",
    "Sinalizacao",
    "Media",
]

for coluna in colunas_numericas:
    df_mobilize[coluna] = (
        df_mobilize[coluna]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df_mobilize[coluna] = pd.to_numeric(
        df_mobilize[coluna],
        errors="coerce",
    )


# =========================================================
# 6.1 VALIDAÇÃO DOS REGISTROS
# =========================================================

# Remove eventuais linhas de rodapé da tabela que não representam
# uma calçada avaliada. Um registro válido precisa ter endereço e
# uma média numérica.
df_mobilize = df_mobilize[
    df_mobilize["Endereco"].fillna("").str.strip().ne("")
    & df_mobilize["Media"].notna()
].copy()

df_mobilize = df_mobilize.reset_index(drop=True)

# A própria fonte informa que o levantamento contém 228 locais.
if len(df_mobilize) != 228:
    raise ValueError(
        f"Quantidade inesperada de registros: {len(df_mobilize)}. "
        "Era esperado encontrar 228 locais."
    )


# =========================================================
# 7. SALVAMENTO
# =========================================================

os.makedirs("data", exist_ok=True)

# QUOTE_ALL evita os problemas de leitura que apareceram no TP2
# quando endereços continham vírgulas.
df_mobilize.to_csv(
    "data/calcadas_mobilize.csv",
    index=False,
    encoding="utf-8-sig",
    quoting=csv.QUOTE_ALL,
)


with open(
    "data/calcadas_mobilize.txt",
    "w",
    encoding="utf-8",
) as arquivo:
    arquivo.write(
        df_mobilize.to_string(index=False)
    )


# Texto usado no gráfico de frequência de termos.
# São utilizados somente campos textuais coletados da tabela.
texto_termos = (
    df_mobilize["Endereco"].fillna("").astype(str)
    + " "
    + df_mobilize["Cidade"].fillna("").astype(str)
)

with open(
    "data/texto_mobilize.txt",
    "w",
    encoding="utf-8",
) as arquivo:
    arquivo.write(
        "\n".join(texto_termos.tolist())
    )


print()
print("Quantidade de registros:", len(df_mobilize))
print("Arquivos criados:")
print("data/calcadas_mobilize.csv")
print("data/calcadas_mobilize.txt")
print("data/texto_mobilize.txt")
