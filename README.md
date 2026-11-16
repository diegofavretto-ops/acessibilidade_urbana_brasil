# Acessibilidade Urbana no Brasil

Projeto desenvolvido na disciplina de **Projeto de Bloco - Inteligência Artificial Aplicada**.

## Etapa atual

**TP4**

## Objetivo

Organizar, visualizar e comparar dados relacionados à acessibilidade urbana no Brasil utilizando Python, Pandas, Streamlit, Web Scraping, FastAPI e um modelo de linguagem executado localmente.

O projeto está relacionado ao **ODS 11 - Cidades e Comunidades Sustentáveis**.

## Evolução do projeto

O projeto foi desenvolvido de forma incremental ao longo dos TPs.

No TP3 foram implementados:

- aplicação Streamlit com múltiplas páginas;
- visualização de frequência de termos;
- API com FastAPI;
- rotas para consulta das UFs;
- registro de observações;
- preparação para integração com modelos de linguagem.

No TP4 foram acrescentados:

- uma segunda página coletada por Web Scraping;
- contingência para indisponibilidade temporária do Mobilize;
- integração de um LLM executado localmente;
- Response Models com Pydantic;
- tratamento de erros HTTP;
- integração entre Streamlit, FastAPI e o modelo local;
- geração de resumos textuais a partir dos indicadores reais do IBGE.

## Fontes de dados

### IBGE

Fonte quantitativa principal:

- Censo Demográfico 2022;
- Características Urbanísticas do Entorno dos Domicílios;
- Tabela SIDRA 9584.

Os percentuais representam características observadas no entorno dos domicílios considerados na pesquisa e não devem ser interpretados diretamente como percentual de todas as ruas de cada UF.

### Mobilize Brasil

O projeto utiliza duas páginas do Mobilize Brasil como fontes complementares obtidas por Web Scraping.

A primeira é:

`Calçadas do Brasil: notas em 228 locais`

A segunda é:

`Panorama das calçadas`

A primeira coleta uma tabela com avaliações numéricas.

A segunda coleta trechos textuais relacionados a temas como:

- calçadas;
- degraus;
- iluminação;
- irregularidades;
- largura;
- obstáculos;
- paisagismo;
- pedestres;
- rampas;
- sinalização.

As duas coletas utilizam Requests e BeautifulSoup.

Durante o desenvolvimento foi observado que o Mobilize pode responder com HTTP 200 e, mesmo assim, apresentar uma página interna de indisponibilidade.

Os scripts foram adaptados para detectar essa situação e manter o último snapshot válido sem sobrescrever os dados existentes.

## Selenium

Selenium foi avaliado, mas não foi necessário para as fontes utilizadas.

Quando as páginas estão disponíveis, os dados de interesse podem ser obtidos diretamente do HTML com Requests e BeautifulSoup.

Por isso, foi mantida a solução mais simples.

## Estrutura

```text
acessibilidade_urbana_brasil/
│
├── app.py
├── api.py
├── comum.py
├── llm_local.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── pages/
│   ├── inicio.py
│   ├── panorama.py
│   ├── comparacoes.py
│   ├── mobilize.py
│   ├── dados.py
│   └── api_llm.py
│
├── 01_business_understanding/
│
├── 02_data_acquisition_understanding/
│   ├── data_summary_report.md
│   ├── scraping_mobilize.py
│   └── scraping_mobilize_panorama.py
│
├── 03_modeling/
│   ├── escolha_modelo_tp4.md
│   ├── integracao_llm_tp4.md
│   ├── baixar_modelo.py
│   └── testar_modelo_local.py
│
├── 04_deployment/
├── 05_customer_acceptance/
├── data/
│
└── models/
    └── qwen2.5-0.5b-instruct/
```

A pasta `models/` está no `.gitignore` porque contém os arquivos locais do modelo.

## Tecnologias

- Python;
- Pandas;
- Streamlit;
- Requests;
- BeautifulSoup;
- FastAPI;
- Uvicorn;
- Pydantic;
- PyTorch;
- Hugging Face Transformers;
- Hugging Face Hub.

## Instalação

Na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Web Scraping

Primeiro levantamento:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize.py
```

Panorama das calçadas:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize_panorama.py
```

Caso o Mobilize esteja temporariamente indisponível, os scripts preservam o último snapshot válido.

## Modelo de linguagem local

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente utilizando PyTorch e Hugging Face Transformers.

Ambiente utilizado:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA não disponível.

Equipamento utilizado nos testes:

- Intel Core i7-1260P;
- aproximadamente 15,6 GB de RAM.

Em um teste com geração de até 80 novos tokens foram observados:

- primeira geração: 9,48 segundos;
- segunda geração: 8,44 segundos.

## Baixar o modelo

```powershell
python 03_modeling\baixar_modelo.py
```

O modelo é salvo em:

`models/qwen2.5-0.5b-instruct`

## Testar o modelo

```powershell
python 03_modeling\testar_modelo_local.py
```

## Executar a FastAPI

```powershell
python -m uvicorn api:app
```

API:

`http://127.0.0.1:8000`

Documentação automática:

`http://127.0.0.1:8000/docs`

## Principais rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica a API |
| GET | `/ufs` | Lista as UFs |
| GET | `/ufs/{estado}` | Consulta uma UF |
| POST | `/observacoes` | Registra uma observação |
| GET | `/observacoes` | Lista observações |
| GET | `/ia/status` | Verifica o modelo local |
| POST | `/ia/resumo-uf` | Gera resumo usando o LLM local |

## Response Models

As respostas da FastAPI são validadas utilizando modelos Pydantic.

Na integração com IA são utilizados:

- `StatusIAResposta`;
- `ResumoUFEntrada`;
- `IndicadoresResumo`;
- `ResumoUFResposta`.

## Tratamento de erros

Foram implementados:

- **404** - UF não encontrada;
- **422** - entrada inválida segundo o Pydantic;
- **503** - modelo local indisponível ou falha de execução;
- **500** - falha inesperada durante a geração.

## Executar o Streamlit

Em outro terminal:

```powershell
python -m streamlit run app.py
```

Aplicação:

`http://localhost:8501`

Para utilizar a página **API e LLM**, a FastAPI também deve estar executando.

## Fluxo da integração

```text
Usuário
   ↓
Streamlit
   ↓
FastAPI
   ↓
dados do IBGE
   ↓
prompt
   ↓
Qwen2.5-0.5B-Instruct local
   ↓
Response Model
   ↓
Streamlit
   ├── tabela
   ├── gráfico
   └── resumo textual
```

O modelo recebe instruções para usar somente os dados fornecidos e evitar conclusões que não sejam suportadas pelos indicadores.

## Documentação complementar

Escolha do modelo:

`03_modeling/escolha_modelo_tp4.md`

Integração do modelo:

`03_modeling/integracao_llm_tp4.md`

Resumo dos dados:

`02_data_acquisition_understanding/data_summary_report.md`

## GitHub

https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil

## Entrega TP4

Arquivo final:

`diego_favretto_PB_TP4.pdf`