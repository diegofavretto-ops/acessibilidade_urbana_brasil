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


# =========================================================
# 2. ACESSO À PÁGINA
# =========================================================

resposta = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30,
)

print(
    "Status da página:",
    resposta.status_code,
)

resposta.raise_for_status()

resposta.encoding = resposta.apparent_encoding


# =========================================================
# 3. BEAUTIFULSOUP
# =========================================================

soup = BeautifulSoup(
    resposta.text,
    "html.parser",
)


# =========================================================
# 4. TERMOS DO PROJETO
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
# 5. EXTRAÇÃO DOS TEXTOS
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

    # Evita registros repetidos.
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


    # Guarda somente textos relacionados
    # ao tema do projeto.
    if categorias_encontradas:

        textos_vistos.add(
            texto
        )

        dados.append(
            {
                "Ordem": len(dados) + 1,

                "Categorias": "; ".join(
                    categorias_encontradas
                ),

                "Texto": texto,

                "Fonte": (
                    "Mobilize Brasil - "
                    "Panorama das calçadas"
                ),

                "URL": URL,
            }
        )


# =========================================================
# 6. DATAFRAME
# =========================================================

df_panorama = pd.DataFrame(
    dados
)


# =========================================================
# 7. VALIDAÇÃO
# =========================================================

if df_panorama.empty:

    raise ValueError(
        "Nenhum trecho relacionado "
        "ao projeto foi encontrado."
    )


# Não existe uma quantidade oficial fixa
# de parágrafos nessa página.
# Apenas verificamos se a coleta encontrou
# conteúdo suficiente para análise.
if len(df_panorama) < 3:

    raise ValueError(
        "Foram encontrados poucos trechos. "
        "A página pode ter sido alterada."
    )


# =========================================================
# 8. SALVAMENTO
# =========================================================

os.makedirs(
    "data",
    exist_ok=True,
)


df_panorama.to_csv(
    "data/mobilize_panorama_calcadas.csv",
    index=False,
    encoding="utf-8-sig",
)


with open(
    "data/mobilize_panorama_calcadas.txt",
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
# 9. RESULTADO
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
    df_panorama["Categorias"]
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
    "Arquivos criados:"
)

print(
    "data/mobilize_panorama_calcadas.csv"
)

print(
    "data/mobilize_panorama_calcadas.txt"
)