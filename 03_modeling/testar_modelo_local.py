from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


# =========================================================
# 1. CAMINHO DO MODELO LOCAL
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_MODELO = (
    BASE_DIR
    / "models"
    / "qwen2.5-0.5b-instruct"
)


print("Modelo local:")
print(PASTA_MODELO)

print()
print("Carregando tokenizer...")


# =========================================================
# 2. TOKENIZER
# =========================================================

tokenizer = AutoTokenizer.from_pretrained(
    PASTA_MODELO,
    local_files_only=True,
)


print("Carregando modelo na CPU...")


# =========================================================
# 3. MODELO
# =========================================================

modelo = AutoModelForCausalLM.from_pretrained(
    PASTA_MODELO,
    local_files_only=True,
    dtype=torch.float32,
)

modelo.to("cpu")

modelo.eval()


# =========================================================
# 4. MENSAGEM DE TESTE
# =========================================================

mensagens = [
    {
        "role": "system",
        "content": (
            "Você é um assistente que responde em português "
            "de forma curta e objetiva."
        ),
    },
    {
        "role": "user",
        "content": (
            "Explique em uma frase o que é acessibilidade urbana."
        ),
    },
]


# =========================================================
# 5. FORMATAÇÃO DO PROMPT
# =========================================================

texto_prompt = tokenizer.apply_chat_template(
    mensagens,
    tokenize=False,
    add_generation_prompt=True,
)


entradas = tokenizer(
    texto_prompt,
    return_tensors="pt",
)


# =========================================================
# 6. GERAÇÃO
# =========================================================

print()
print("Gerando resposta...")

with torch.no_grad():

    saida = modelo.generate(
        **entradas,
        max_new_tokens=80,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )


# =========================================================
# 7. PEGAR SOMENTE A RESPOSTA NOVA
# =========================================================

tokens_entrada = entradas["input_ids"].shape[1]

tokens_resposta = saida[0][tokens_entrada:]


resposta = tokenizer.decode(
    tokens_resposta,
    skip_special_tokens=True,
)


# =========================================================
# 8. RESULTADO
# =========================================================

print()
print("Resposta do modelo:")
print(resposta)