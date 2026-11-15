import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. FONTE
# =========================================================

URL = (
    "https://www.mobilize.org.br/"
    "campanhas/calcadas-do-brasil/levantamento"
)

CAMINHO_CSV = (
    "data/mobilize_panorama_calcadas.csv"
)

CAMINHO_TXT = (
    "data/mobilize_panorama_calcadas.txt"
)


# =========================================================
# 2. FUNÇÃO PARA PRESERVAR O SNAPSHOT
# =========================================================

def usar_snapshot_anterior(motivo):

    print()
    print(
        "Aviso:",
        motivo,
    )


    if os.path.exists(
        CAMINHO_CSV
    ):

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
            "Quantidade de trechos preservados:",
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
# 3. ACESSO À PÁGINA
# =========================================================

try:

    resposta = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
        timeout=30,
    )


except requests.RequestException:

    usar_snapshot_anterior(
        "Não foi possível acessar a página "
        "Panorama das Calçadas."
    )


print(
    "Status da página:",
    resposta.status_code,
)


if resposta.status_code != 200:

    usar_snapshot_anterior(
        (
            "O Mobilize respondeu com "
            f"status {resposta.status_code}."
        )
    )


# =========================================================
# 4. BEAUTIFULSOUP
# =========================================================

soup = BeautifulSoup(
    resposta.content,
    "html.parser",
)


texto_pagina = soup.get_text(
    " ",
    strip=True,
)


# O site pode responder HTTP 200
# exibindo internamente uma página de erro.
if (
    "Esta página não pode ser exibida no momento"
    in texto_pagina
):

    usar_snapshot_anterior(
        "O Mobilize está temporariamente "
        "indisponível para coleta."
    )


# =========================================================
# 5. TERMOS DO PROJETO
# =========================================================

categorias = {

    "Irregularidades": [
        "irregularidade",
        "irregularidades",
        "piso",
    ],

    "Degraus": [
        "degrau",
        "degraus",
    ],

    "Largura": [
        "largura",
    ],

    "Rampas": [
        "rampa",
        "rampas",
    ],

    "Obstáculos": [
        "obstáculo",
        "obstáculos",
    ],

    "Iluminação": [
        "iluminação",
    ],

    "Sinalização": [
        "sinalização",
    ],

    "Paisagismo": [
        "paisagismo",
    ],

    "Pedestres": [
        "pedestre",
        "pedestres",
    ],

    "Calçadas": [
        "calçada",
        "calçadas",
    ],
}


# =========================================================
# 6. EXTRAÇÃO DOS TEXTOS
# =========================================================

dados = []

textos_vistos = set()


elementos = soup.find_all(
    [
        "p",
        "li",
    ]
)


for elemento in elementos:

    texto = elemento.get_text(
        " ",
        strip=True,
    )


    # Ignora textos muito pequenos.
    if len(texto) < 30:
        continue


    # Evita duplicação.
    if texto in textos_vistos:
        continue


    texto_minusculo = (
        texto.casefold()
    )


    categorias_encontradas = []


    for categoria, termos in categorias.items():

        for termo in termos:

            if (
                termo.casefold()
                in texto_minusculo
            ):

                categorias_encontradas.append(
                    categoria
                )

                break


    if categorias_encontradas:

        textos_vistos.add(
            texto
        )


        dados.append(
            {
                "Ordem":
                    len(dados) + 1,

                "Categorias":
                    "; ".join(
                        categorias_encontradas
                    ),

                "Texto":
                    texto,

                "Fonte":
                    (
                        "Mobilize Brasil - "
                        "Panorama das calçadas"
                    ),

                "URL":
                    URL,
            }
        )


# =========================================================
# 7. DATAFRAME
# =========================================================

df_panorama = pd.DataFrame(
    dados
)


# =========================================================
# 8. VALIDAÇÃO
# =========================================================

if df_panorama.empty:

    usar_snapshot_anterior(
        "Nenhum trecho relacionado ao projeto "
        "foi encontrado na página atual."
    )


if len(df_panorama) < 3:

    usar_snapshot_anterior(
        (
            "Foram encontrados apenas "
            f"{len(df_panorama)} trechos. "
            "A estrutura da página pode ter sido alterada."
        )
    )


# =========================================================
# 9. SALVAMENTO
# =========================================================

os.makedirs(
    "data",
    exist_ok=True,
)


df_panorama.to_csv(
    CAMINHO_CSV,
    index=False,
    encoding="utf-8-sig",
)


with open(
    CAMINHO_TXT,
    "w",
    encoding="utf-8",
) as arquivo:

    for _, linha in df_panorama.iterrows():

        arquivo.write(
            f"{linha['Categorias']}\n"
        )

        arquivo.write(
            f"{linha['Texto']}\n\n"
        )


# =========================================================
# 10. RESULTADO
# =========================================================

print()

print(
    "Quantidade de trechos coletados:",
    len(df_panorama),
)

print()

print(
    "Categorias encontradas:"
)


categorias_encontradas = (
    df_panorama[
        "Categorias"
    ]
    .str.split("; ")
    .explode()
    .drop_duplicates()
    .sort_values()
)


for categoria in categorias_encontradas:

    print(
        "-",
        categoria,
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