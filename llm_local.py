from functools import lru_cache
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# =========================================================
# 1. CONFIGURAÇÃO DO MODELO
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

PASTA_MODELO = (
    BASE_DIR
    / "models"
    / "qwen2.5-0.5b-instruct"
)

NOME_MODELO = "Qwen/Qwen2.5-0.5B-Instruct"

DISPOSITIVO = "cpu"


# =========================================================
# 2. TOKENIZER
# =========================================================

@lru_cache(maxsize=1)
def carregar_tokenizer():

    if not PASTA_MODELO.exists():
        raise FileNotFoundError(
            "O modelo local não foi encontrado."
        )

    tokenizer = AutoTokenizer.from_pretrained(
        PASTA_MODELO,
        local_files_only=True,
    )

    return tokenizer


# =========================================================
# 3. MODELO
# =========================================================

@lru_cache(maxsize=1)
def carregar_modelo():

    if not PASTA_MODELO.exists():
        raise FileNotFoundError(
            "O modelo local não foi encontrado."
        )

    modelo = AutoModelForCausalLM.from_pretrained(
        PASTA_MODELO,
        local_files_only=True,
        dtype=torch.float32,
    )

    modelo.to(
        DISPOSITIVO
    )

    modelo.eval()

    return modelo


# =========================================================
# 4. STATUS
# =========================================================

def obter_status_modelo():

    return {
        "modelo": NOME_MODELO,
        "dispositivo": DISPOSITIVO,
        "arquivos_locais": PASTA_MODELO.exists(),
    }


# =========================================================
# 5. GERAÇÃO DE TEXTO
# =========================================================

def gerar_resposta(
    mensagem_usuario,
    max_new_tokens=160,
):

    tokenizer = carregar_tokenizer()

    modelo = carregar_modelo()


    mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um assistente de análise de dados. "
                "Responda em português do Brasil, de forma "
                "clara, curta e objetiva. "
                "Não invente dados que não foram fornecidos."
            ),
        },
        {
            "role": "user",
            "content": mensagem_usuario,
        },
    ]


    prompt = tokenizer.apply_chat_template(
        mensagens,
        tokenize=False,
        add_generation_prompt=True,
    )


    entradas = tokenizer(
        prompt,
        return_tensors="pt",
    )


    entradas = {
        chave: valor.to(DISPOSITIVO)
        for chave, valor
        in entradas.items()
    }


    with torch.no_grad():

        saida = modelo.generate(
            **entradas,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )


    quantidade_tokens_entrada = (
        entradas["input_ids"].shape[1]
    )


    tokens_resposta = (
        saida[0][
            quantidade_tokens_entrada:
        ]
    )


    resposta = tokenizer.decode(
        tokens_resposta,
        skip_special_tokens=True,
    )


    return resposta.strip()