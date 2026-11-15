import csv
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. FONTES
# =========================================================

URL_NORMAL = (
    "https://www.mobilize.org.br/"
    "estatisticas/31/"
    "calcadas-do-brasil-ficam-com-media-34.html"
)

URL_IMPRESSAO = (
    "https://www.mobilize.org.br/"
    "estatisticas/31/"
    "calcadas-do-brasil-ficam-com-media-34.html"
    "?print=s"
)

CAMINHO_CSV = "data/calcadas_mobilize.csv"
CAMINHO_TXT = "data/calcadas_mobilize.txt"
CAMINHO_TEXTO = "data/texto_mobilize.txt"


# =========================================================
# 2. FUNÇÃO PARA USAR SNAPSHOT ANTERIOR
# =========================================================

def usar_snapshot_anterior(motivo):
    print()
    print("Aviso:", motivo)

    if os.path.exists(CAMINHO_CSV):

        df_existente = pd.read_csv(
            CAMINHO_CSV
        )

        print()
        print(
            "O último arquivo válido já existente "
            "será mantido."
        )

        print(
            "Arquivo:",
            CAMINHO_CSV,
        )

        print(
            "Quantidade de registros preservados:",
            len(df_existente),
        )

        print(
            "Nenhum dado anterior foi sobrescrito."
        )

        raise SystemExit(0)

    raise RuntimeError(
        "A fonte está indisponível e não existe "
        "um snapshot local anterior."
    )


# =========================================================
# 3. TENTATIVA DE ACESSO
# =========================================================

tabela_dados = None
url_utilizada = None

urls = [
    URL_NORMAL,
    URL_IMPRESSAO,
]


for url in urls:

    print()
    print(
        "Tentando acessar:",
        url,
    )

    try:

        resposta = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
            },
            timeout=30,
        )

    except requests.RequestException:

        print(
            "Não foi possível acessar esta URL."
        )

        continue


    print(
        "Status da página:",
        resposta.status_code,
    )


    if resposta.status_code != 200:
        continue


    soup = BeautifulSoup(
        resposta.content,
        "html.parser",
    )


    texto_pagina = soup.get_text(
        " ",
        strip=True,
    )


    # O Mobilize pode responder HTTP 200,
    # mas mostrar internamente uma página de erro.
    if (
        "Esta página não pode ser exibida no momento"
        in texto_pagina
    ):

        print(
            "O Mobilize retornou uma página "
            "temporariamente indisponível."
        )

        continue


    tabelas = soup.find_all(
        "table"
    )


    for tabela in tabelas:

        texto_tabela = tabela.get_text(
            " ",
            strip=True,
        )

        texto_normalizado = (
            texto_tabela.casefold()
        )


        if (
            "endereço" in texto_normalizado
            and "rampas" in texto_normalizado
            and "arborização" in texto_normalizado
        ):

            tabela_dados = tabela
            url_utilizada = url

            break


    if tabela_dados is not None:
        break


# =========================================================
# 4. CONTINGÊNCIA
# =========================================================

if tabela_dados is None:

    usar_snapshot_anterior(
        "A tabela do Mobilize não pôde ser "
        "obtida nesta execução."
    )


print()
print(
    "Tabela encontrada em:",
    url_utilizada,
)


# =========================================================
# 5. EXTRAÇÃO DAS LINHAS
# =========================================================

dados = []


for linha in tabela_dados.find_all(
    "tr"
):

    celulas = linha.find_all(
        "td"
    )

    valores = []


    for celula in celulas:

        texto = celula.get_text(
            " ",
            strip=True,
        )

        valores.append(
            texto
        )


    # Algumas versões da página possuem
    # uma primeira coluna que não é utilizada.
    if len(valores) == 12:

        valores = valores[1:]


    if (
        len(valores) == 11
        and valores[0].strip()
        and valores[-1].strip()
    ):

        dados.append(
            valores
        )


# =========================================================
# 6. DATAFRAME
# =========================================================

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
# 7. SEPARAÇÃO DE CIDADE/LOCALIDADE
# =========================================================

def separar_cidade(texto):

    texto = str(
        texto
    ).strip()


    posicao_virgula = texto.rfind(
        ","
    )

    posicao_traco = texto.rfind(
        " - "
    )


    if posicao_virgula > posicao_traco:

        endereco = texto[
            :posicao_virgula
        ].strip()

        cidade = texto[
            posicao_virgula + 1:
        ].strip()


    elif posicao_traco != -1:

        endereco = texto[
            :posicao_traco
        ].strip()

        cidade = texto[
            posicao_traco + 3:
        ].strip()


    else:

        endereco = texto
        cidade = ""


    return pd.Series(
        [
            endereco,
            cidade,
        ]
    )


if not df_mobilize.empty:

    df_mobilize[
        [
            "Endereco",
            "Cidade",
        ]
    ] = (
        df_mobilize[
            "Endereco"
        ].apply(
            separar_cidade
        )
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
# 8. CONVERSÃO PARA NÚMEROS
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
        .str.replace(
            ",",
            ".",
            regex=False,
        )
    )


    df_mobilize[coluna] = (
        pd.to_numeric(
            df_mobilize[coluna],
            errors="coerce",
        )
    )


# =========================================================
# 9. VALIDAÇÃO DOS REGISTROS
# =========================================================

df_mobilize = df_mobilize[
    df_mobilize[
        "Endereco"
    ]
    .fillna("")
    .str.strip()
    .ne("")

    &

    df_mobilize[
        "Media"
    ].notna()
].copy()


df_mobilize = (
    df_mobilize
    .reset_index(
        drop=True
    )
)


# O levantamento original informa 228 locais.
if len(df_mobilize) != 228:

    usar_snapshot_anterior(
        (
            "A coleta atual encontrou "
            f"{len(df_mobilize)} registros, "
            "mas eram esperados 228."
        )
    )


# =========================================================
# 10. SALVAMENTO
# =========================================================

os.makedirs(
    "data",
    exist_ok=True,
)


df_mobilize.to_csv(
    CAMINHO_CSV,
    index=False,
    encoding="utf-8-sig",
    quoting=csv.QUOTE_ALL,
)


with open(
    CAMINHO_TXT,
    "w",
    encoding="utf-8",
) as arquivo:

    arquivo.write(
        df_mobilize.to_string(
            index=False
        )
    )


# =========================================================
# 11. TEXTO PARA FREQUÊNCIA DE TERMOS
# =========================================================

texto_termos = (
    df_mobilize[
        "Endereco"
    ]
    .fillna("")
    .astype(str)

    + " "

    + df_mobilize[
        "Cidade"
    ]
    .fillna("")
    .astype(str)
)


with open(
    CAMINHO_TEXTO,
    "w",
    encoding="utf-8",
) as arquivo:

    arquivo.write(
        "\n".join(
            texto_termos.tolist()
        )
    )


# =========================================================
# 12. RESULTADO
# =========================================================

print()

print(
    "Quantidade de registros:",
    len(df_mobilize),
)

print()

print(
    "Arquivos atualizados:"
)

print(
    CAMINHO_CSV
)

print(
    CAMINHO_TXT
)

print(
    CAMINHO_TEXTO
)