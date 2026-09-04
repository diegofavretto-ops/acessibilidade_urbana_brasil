import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. ENDEREÇO DA PÁGINA
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
    timeout=30
)


print(
    "Status da página:",
    resposta.status_code
)


# Interrompe o programa caso a página retorne erro
resposta.raise_for_status()


# Ajuda na leitura correta de acentos
resposta.encoding = resposta.apparent_encoding


# =========================================================
# 3. BEAUTIFULSOUP
# =========================================================

soup = BeautifulSoup(
    resposta.text,
    "html.parser"
)


# Procura todas as tabelas existentes na página
tabelas = soup.find_all(
    "table"
)


tabela_dados = None


# =========================================================
# 4. LOCALIZA A TABELA CORRETA
# =========================================================

for tabela in tabelas:

    texto_tabela = tabela.get_text(
        " ",
        strip=True
    )

    if (
        "Endereço" in texto_tabela
        and
        "Rampas" in texto_tabela
        and
        "Arborização" in texto_tabela
    ):

        tabela_dados = tabela

        break


if tabela_dados is None:

    raise ValueError(
        "A tabela esperada não foi encontrada na página."
    )


# =========================================================
# 5. EXTRAÇÃO DAS LINHAS DA TABELA
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
            strip=True
        )

        valores.append(
            texto
        )


    # A tabela possui uma primeira coluna
    # que não será utilizada no projeto
    if len(valores) == 12:

        valores = valores[1:]


    # Somente adiciona linhas com os 11 campos esperados
    if len(valores) == 11:

        dados.append(
            valores
        )


# =========================================================
# 6. CRIAÇÃO DO DATAFRAME
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
    "Media"
]


df_mobilize = pd.DataFrame(
    dados,
    columns=colunas
)


# =========================================================
# 7. FUNÇÃO PARA SEPARAR A CIDADE
# =========================================================

def separar_cidade(texto):

    texto = str(
        texto
    ).strip()


    # Procura a última vírgula
    posicao_virgula = texto.rfind(
        ","
    )


    # Procura o último traço
    posicao_traco = texto.rfind(
        " - "
    )


    # -----------------------------------------------------
    # CASO 1
    # A última vírgula está mais à direita que o traço
    #
    # Exemplo:
    #
    # R. Quinze de Novembro - Sé,São Paulo
    #
    # Endereço:
    # R. Quinze de Novembro - Sé
    #
    # Cidade:
    # São Paulo
    # -----------------------------------------------------

    if (
        posicao_virgula
        >
        posicao_traco
    ):

        endereco = texto[
            :posicao_virgula
        ].strip()


        cidade = texto[
            posicao_virgula + 1:
        ].strip()


    # -----------------------------------------------------
    # CASO 2
    # O último traço aparece mais à direita
    #
    # Exemplo:
    #
    # Av. Bezerra de Menezes - Fortaleza
    #
    # Endereço:
    # Av. Bezerra de Menezes
    #
    # Cidade:
    # Fortaleza
    # -----------------------------------------------------

    elif posicao_traco != -1:

        endereco = texto[
            :posicao_traco
        ].strip()


        cidade = texto[
            posicao_traco + 3:
        ].strip()


    # -----------------------------------------------------
    # CASO 3
    # Não encontrou vírgula nem traço
    # -----------------------------------------------------

    else:

        endereco = texto

        cidade = ""


    return pd.Series(
        [
            endereco,
            cidade
        ]
    )


# =========================================================
# 8. APLICA A SEPARAÇÃO
# =========================================================

df_mobilize[
    [
        "Endereco",
        "Cidade"
    ]
] = df_mobilize[
    "Endereco"
].apply(
    separar_cidade
)


# =========================================================
# 9. ORGANIZA A ORDEM DAS COLUNAS
# =========================================================

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
        "Media"
    ]
]


# =========================================================
# 10. CONVERSÃO DOS VALORES PARA NÚMEROS
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
    "Media"
]


for coluna in colunas_numericas:

    # Troca vírgula decimal por ponto
    df_mobilize[coluna] = (
        df_mobilize[coluna]
        .astype(str)
        .str.replace(
            ",",
            ".",
            regex=False
        )
    )


    # Transforma texto em número
    df_mobilize[coluna] = pd.to_numeric(
        df_mobilize[coluna],
        errors="coerce"
    )


# =========================================================
# 11. CRIA A PASTA DATA
# =========================================================

os.makedirs(
    "data",
    exist_ok=True
)


# =========================================================
# 12. SALVA O CSV
# =========================================================

try:

    df_mobilize.to_csv(
        "data/calcadas_mobilize.csv",
        index=False,
        encoding="utf-8-sig"
    )


except PermissionError:

    print()
    print(
        "ERRO: não foi possível salvar "
        "data/calcadas_mobilize.csv"
    )

    print(
        "Feche o arquivo CSV no Excel "
        "e execute o programa novamente."
    )

    raise


# =========================================================
# 13. SALVA O TXT
# =========================================================

with open(
    "data/calcadas_mobilize.txt",
    "w",
    encoding="utf-8"
) as arquivo:

    arquivo.write(
        df_mobilize.to_string(
            index=False
        )
    )


# =========================================================
# 14. RESULTADO DO SCRAPING
# =========================================================

print()

print(
    "Quantidade de registros:",
    len(df_mobilize)
)


print()

print(
    "Arquivos criados:"
)


print(
    "data/calcadas_mobilize.csv"
)


print(
    "data/calcadas_mobilize.txt"
)


# =========================================================
# 15. VERIFICAÇÃO DAS CIDADES
# =========================================================

print()

print(
    "Cidades encontradas:"
)


print(
    df_mobilize[
        "Cidade"
    ]
    .value_counts(
        dropna=False
    )
    .sort_index()
)


# =========================================================
# 16. MOSTRA AS PRIMEIRAS LINHAS
# =========================================================

print()

print(
    "Primeiras linhas da base:"
)


print(
    df_mobilize[
        [
            "Endereco",
            "Cidade"
        ]
    ]
    .head(20)
    .to_string(
        index=False
    )
)