# Integração do LLM local - TP4

## 1. Modelo utilizado

O projeto utiliza o modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente, sem utilização de uma API externa de inteligência artificial.

A justificativa detalhada da escolha está registrada em:

`03_modeling/escolha_modelo_tp4.md`

## 2. Ambiente utilizado

Durante o desenvolvimento foram verificados:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA disponível: não.

O equipamento utilizado possui:

- processador Intel Core i7-1260P;
- aproximadamente 15,6 GB de RAM.

O modelo foi baixado para:

`models/qwen2.5-0.5b-instruct`

Essa pasta está configurada no `.gitignore`, portanto os pesos do modelo não são enviados ao GitHub.

## 3. Instalação

As dependências são instaladas pelo arquivo:

`requirements.txt`

Comando:

```powershell
python -m pip install -r requirements.txt
```

As principais bibliotecas relacionadas à integração são:

- `torch`;
- `transformers`;
- `huggingface_hub`;
- `fastapi`;
- `uvicorn`;
- `pydantic`.

## 4. Download do modelo

O download é realizado pelo arquivo:

`03_modeling/baixar_modelo.py`

Comando:

```powershell
python 03_modeling\baixar_modelo.py
```

O modelo é armazenado em:

`models/qwen2.5-0.5b-instruct`

## 5. Teste isolado do modelo

Antes de integrar o modelo à FastAPI, foi realizado um teste utilizando:

`03_modeling/testar_modelo_local.py`

O carregamento utiliza:

- `AutoTokenizer`;
- `AutoModelForCausalLM`;
- `local_files_only=True`;
- `modelo.eval()`;
- `torch.no_grad()`.

O projeto utiliza o modelo somente para inferência.

Não é realizado treinamento ou fine-tuning.

## 6. Módulo `llm_local.py`

A lógica principal do modelo está no arquivo:

`llm_local.py`

Principais funções:

- `carregar_tokenizer()`;
- `carregar_modelo()`;
- `obter_status_modelo()`;
- `gerar_resposta()`.

O carregamento utiliza:

```python
@lru_cache(maxsize=1)
```

Assim, depois da primeira execução, o modelo permanece em memória e pode ser reutilizado nas próximas chamadas.

## 7. Medição de desempenho

Foi realizado um teste com geração de até 80 novos tokens.

Equipamento:

- Intel Core i7-1260P;
- aproximadamente 15,6 GB de RAM;
- execução em CPU;
- CUDA não disponível.

Resultados:

- primeira geração: 9,48 segundos;
- segunda geração: 8,44 segundos.

O resultado mostrou que o modelo pode ser utilizado localmente no equipamento disponível sem GPU dedicada.

## 8. Integração com FastAPI

A integração está no arquivo:

`api.py`

Foram acrescentadas duas rotas principais de IA.

### GET `/ia/status`

Retorna:

- nome do modelo;
- dispositivo utilizado;
- existência dos arquivos locais.

### POST `/ia/resumo-uf`

Recebe uma Unidade da Federação.

Exemplo:

```json
{
  "estado": "Santa Catarina"
}
```

A API consulta os indicadores do IBGE e envia ao modelo:

- calçada/passeio;
- calçadas sem obstáculos;
- rampas;
- arborização.

## 9. Regras do prompt

O modelo recebe instruções para:

1. utilizar somente os dados fornecidos;
2. não inventar valores;
3. não utilizar informações externas;
4. não classificar a UF simplesmente como acessível ou inacessível;
5. não transformar os percentuais em percentual de ruas;
6. considerar o contexto metodológico dos indicadores;
7. responder em português do Brasil;
8. produzir um texto curto;
9. não criar um índice geral de acessibilidade.

## 10. Response Models

Na integração com IA foram definidos:

- `StatusIAResposta`;
- `ResumoUFEntrada`;
- `IndicadoresResumo`;
- `ResumoUFResposta`.

A resposta contém:

- estado;
- região;
- modelo;
- dispositivo;
- indicadores;
- resumo.

Dessa forma, a FastAPI não devolve apenas um texto livre.

A resposta segue uma estrutura definida e validada pelo Pydantic.

## 11. Tratamento de erros

Foram implementados:

### HTTP 404

Utilizado quando a Unidade da Federação não existe na base.

### HTTP 422

Utilizado quando a entrada não passa pela validação do Pydantic.

### HTTP 503

Utilizado quando:

- o modelo local não está disponível;
- os arquivos não podem ser carregados;
- ocorre falha durante a execução.

### HTTP 500

Utilizado para uma falha inesperada durante a geração.

## 12. Integração com Streamlit

A página:

`pages/api_llm.py`

permite:

- verificar o status da API;
- verificar o modelo local;
- consultar indicadores;
- visualizar tabela;
- visualizar gráfico;
- gerar resumo com IA local;
- visualizar o texto gerado;
- registrar observações.

Os dados recebidos da FastAPI não são apresentados apenas como JSON.

Eles são usados diretamente nos componentes da interface.

## 13. Fluxo completo

```text
Usuário
   ↓
Streamlit
   ↓
FastAPI
   ↓
dados do IBGE
   ↓
seleção dos indicadores
   ↓
construção do prompt
   ↓
Qwen2.5-0.5B-Instruct
   ↓
Response Model
   ↓
FastAPI
   ↓
Streamlit
   ├── tabela
   ├── gráfico
   └── resumo
```

## 14. Como executar

FastAPI:

```powershell
python -m uvicorn api:app
```

Streamlit, em outro terminal:

```powershell
python -m streamlit run app.py
```

## 15. Resultado

O TP4 integrou de forma funcional um LLM local ao projeto.

A solução:

- executa o modelo localmente;
- não utiliza API externa de IA para gerar os textos;
- utiliza Hugging Face Transformers;
- utiliza dados reais do projeto;
- disponibiliza a funcionalidade por FastAPI;
- utiliza Response Models;
- valida as entradas;
- trata erros HTTP;
- devolve a resposta ao Streamlit;
- utiliza os resultados em tabelas, gráficos e texto.