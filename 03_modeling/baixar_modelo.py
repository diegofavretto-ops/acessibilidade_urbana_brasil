from pathlib import Path

from huggingface_hub import snapshot_download


# =========================================================
# 1. MODELO
# =========================================================

MODELO_ID = "Qwen/Qwen2.5-0.5B-Instruct"


# =========================================================
# 2. PASTA LOCAL
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_MODELO = (
    BASE_DIR
    / "models"
    / "qwen2.5-0.5b-instruct"
)


# =========================================================
# 3. INFORMAÇÕES
# =========================================================

print(
    "Modelo:",
    MODELO_ID,
)

print(
    "Pasta de destino:",
    PASTA_MODELO,
)

print()

print(
    "Iniciando download..."
)


# =========================================================
# 4. DOWNLOAD
# =========================================================

snapshot_download(
    repo_id=MODELO_ID,
    local_dir=PASTA_MODELO,
)


# =========================================================
# 5. FINALIZAÇÃO
# =========================================================

print()

print(
    "Download concluído."
)

print(
    "Modelo salvo em:",
    PASTA_MODELO,
)