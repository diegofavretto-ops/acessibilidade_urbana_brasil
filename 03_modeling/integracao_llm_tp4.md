# Integração do LLM local - TP4

## 1. Modelo utilizado

O projeto utiliza o modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente, sem utilização de uma API externa de
inteligência artificial.

A justificativa detalhada da escolha está registrada em:

`03_modeling/escolha_modelo_tp4.md`

## 2. Ambiente utilizado

Durante o desenvolvimento do TP4 foram verificados:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA disponível: não.

O modelo foi baixado para:

`models/qwen2.5-0.5b-instruct`

Essa pasta está configurada no `.gitignore` e, portanto, os pesos do modelo não
são enviados ao GitHub.

O arquivo principal de pesos utilizado localmente é:

`model.safetensors`

## 3. Instalação das bibliotecas

Após criar e ativar o ambiente virtual, as dependências são instaladas por meio
do arquivo `requirements.txt`.

Comando:

```powershell
python -m pip install -r requirements.txt