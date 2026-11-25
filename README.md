# Acessibilidade Urbana no Brasil

Projeto desenvolvido por Diego Favretto na disciplina de Projeto de Bloco — Inteligência Artificial Aplicada, do curso de Ciência de Dados.

## 1. Apresentação

A aplicação reúne dados públicos e informações coletadas na web para facilitar a consulta, a visualização e a interpretação de indicadores relacionados à acessibilidade urbana no Brasil.

O projeto integra análise de dados, Web Scraping, desenvolvimento de interfaces, APIs e Inteligência Artificial Generativa.

A proposta está relacionada ao ODS 11 — Cidades e Comunidades Sustentáveis — e à dimensão Social do ESG.

## 2. Problema e objetivo

Embora existam informações públicas sobre as condições do ambiente urbano brasileiro, a consulta e a comparação desses dados nem sempre são simples.

O projeto tem como objetivo reunir essas informações em uma aplicação interativa, permitindo identificar diferenças entre estados e regiões e consultar informações complementares sobre as condições das calçadas.

A Inteligência Artificial é utilizada como ferramenta complementar para interpretação dos indicadores e sumarização dos textos coletados.

## 3. Funcionalidades

A aplicação permite:

- consultar indicadores das 27 Unidades da Federação;
- visualizar rankings estaduais;
- comparar estados e regiões;
- explorar gráficos, tabelas e indicadores;
- analisar avaliações de calçadas coletadas do Mobilize Brasil;
- consultar frequência de termos e categorias;
- realizar upload e download de dados;
- consultar informações por meio de uma API;
- registrar observações complementares;
- gerar resumos dos indicadores do IBGE com IA local;
- solicitar a sumarização automatizada dos textos coletados;
- consultar as evidências utilizadas na sumarização.

## 4. Fontes de dados

### IBGE

Fonte quantitativa principal:

- Censo Demográfico 2022;
- Características Urbanísticas do Entorno dos Domicílios;
- Tabela SIDRA 9584.

Disponível em:

https://sidra.ibge.gov.br/tabela/9584

Os indicadores analisados incluem calçadas, rampas, obstáculos, arborização, iluminação pública, pontos de transporte coletivo e vias para bicicletas.

Os percentuais representam características observadas no entorno dos domicílios considerados na pesquisa, não devendo ser interpretados como percentuais de todas as ruas de cada estado.

### Mobilize Brasil

São utilizadas duas fontes complementares:

**Calçadas do Brasil: notas em 228 locais**

https://www.mobilize.org.br/estatisticas/31/calcadas-do-brasil-ficam-com-media-34.html

**Panorama das calçadas**

https://www.mobilize.org.br/campanhas/calcadas-do-brasil/levantamento

As informações foram coletadas utilizando Requests e BeautifulSoup.

A primeira fonte contém avaliações numéricas. A segunda contém textos relacionados às condições das calçadas, organizados em categorias para consulta e sumarização.

As fontes possuem metodologias diferentes e não são utilizadas como bases diretamente equivalentes.

## 5. Metodologia

O projeto foi organizado de acordo com o Team Data Science Process (TDSP).

| Fase | Atividades |
|---|---|
| Business Understanding | Definição do problema, objetivos e contexto. |
| Data Acquisition and Understanding | Coleta, tratamento e análise dos dados. |
| Modeling | Análise exploratória, integração do LLM e Engenharia de Prompt. |
| Deployment | Integração do Streamlit, FastAPI e modelo local. |
| Customer Acceptance | Testes, avaliação dos resultados e identificação das limitações. |

## 6. Tecnologias utilizadas

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
- Hugging Face Hub;
- Git e GitHub.

## 7. Arquitetura

```text
                 USUÁRIO
                    |
                STREAMLIT
                    |
                 FASTAPI
              /     |     \
           IBGE  MOBILIZE  QWEN
             \      |      /
               RESULTADOS
                    |
                STREAMLIT
```

O Streamlit é responsável pela interface, pelos filtros e pela apresentação das informações.

A FastAPI disponibiliza rotas de consulta aos dados e geração de textos com Inteligência Artificial.

O módulo `llm_local.py` é responsável pelo carregamento e pela execução do modelo de linguagem.

O dashboard também realiza análises diretamente sobre os arquivos de dados disponíveis no projeto.

## 8. Estrutura do projeto

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
│   └── project_charter.md
│
├── 02_data_acquisition_understanding/
│   ├── data_summary_report.md
│   ├── scraping_mobilize.py
│   ├── scraping_mobilize_panorama.py
│   └── ufs_streamlit_resumo.csv
│
├── 03_modeling/
│   ├── baixar_modelo.py
│   ├── testar_modelo_local.py
│   ├── escolha_modelo.md
│   ├── integracao_llm.md
│   ├── prompt_engineering.md
│   └── modeling_report.md
│
├── 04_deployment/
│   └── deployment_report.md
│
├── 05_customer_acceptance/
│   ├── acceptance_report.md
│   └── evidencias/
│
├── data/
│
└── models/
    └── qwen2.5-0.5b-instruct/
```

A estrutura apresenta os principais arquivos do projeto.

A pasta `models/` é criada localmente após o download do modelo e não é enviada ao GitHub.

## 9. Instalação

### Clonar o repositório

```powershell
git clone https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil.git
```

```powershell
cd acessibilidade_urbana_brasil
```

### Criar o ambiente virtual

```powershell
python -m venv .venv
```

### Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

## 10. Coleta de dados por Web Scraping

O projeto contém os arquivos coletados durante o desenvolvimento.

Caso seja necessário atualizar os dados, executar:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize.py
```

Para atualizar os textos:

```powershell
python 02_data_acquisition_understanding\scraping_mobilize_panorama.py
```

Os scripts utilizam Requests e BeautifulSoup.

Selenium foi considerado, mas não foi necessário para as páginas utilizadas, pois os dados podem ser obtidos diretamente do HTML quando as páginas estão disponíveis.

Caso o site esteja temporariamente indisponível, os scripts procuram preservar o último conjunto válido de dados.

## 11. Modelo de linguagem

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

Características:

- aproximadamente 490 milhões de parâmetros;
- execução local em CPU;
- suporte a instruções em português;
- licença Apache 2.0;
- integração com Hugging Face Transformers.

Referência:

https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct

A escolha considerou a possibilidade de executar o modelo em um computador pessoal, sem necessidade de contratar uma API externa de Inteligência Artificial.

Não foi realizado treinamento ou fine-tuning.

### Download do modelo

```powershell
python 03_modeling\baixar_modelo.py
```

### Teste isolado

```powershell
python 03_modeling\testar_modelo_local.py
```

## 12. Executar a aplicação

São necessários dois terminais com o ambiente virtual ativado para utilizar todas as funcionalidades.

### Terminal 1 — FastAPI

```powershell
python -m uvicorn api:app
```

Endereço da API:

http://127.0.0.1:8000

Documentação automática:

http://127.0.0.1:8000/docs

### Terminal 2 — Streamlit

```powershell
python -m streamlit run app.py
```

Endereço da aplicação:

http://localhost:8501

A FastAPI deve permanecer em execução durante a utilização das funcionalidades de integração e Inteligência Artificial.

## 13. Rotas da API

| Método | Rota | Funcionalidade |
|---|---|---|
| GET | `/` | Verificar a API |
| GET | `/ufs` | Listar as UFs |
| GET | `/ufs/{estado}` | Consultar uma UF |
| POST | `/observacoes` | Registrar observação |
| GET | `/observacoes` | Listar observações |
| GET | `/ia/status` | Verificar o modelo local |
| POST | `/ia/resumo-uf` | Gerar resumo dos indicadores |
| POST | `/ia/resumo-mobilize` | Sumarizar textos coletados |

A API utiliza modelos Pydantic para definição e validação da estrutura dos dados.

## 14. Engenharia de Prompt

Foram implementados prompts estruturados para duas funcionalidades principais:

### Análise de indicadores do IBGE

O modelo recebe os indicadores da Unidade da Federação selecionada e instruções para produzir um resumo utilizando somente as informações fornecidas.

### Sumarização de textos do Mobilize

O usuário seleciona uma categoria.

A aplicação recupera os textos associados, organiza as evidências e envia as informações ao modelo.

A resposta passa por uma verificação baseada em expressões específicas. Quando determinadas extrapolações são identificadas, o sistema realiza uma segunda tentativa de geração.

Caso a resposta continue apresentando essas expressões, é utilizada uma saída alternativa.

A interface identifica o método utilizado e disponibiliza os textos originais para conferência.

Essa verificação não garante a fidelidade semântica das respostas.

## 15. Resultados e testes

Os testes confirmaram:

- execução local do modelo Qwen;
- integração entre Streamlit e FastAPI;
- geração de textos a partir dos indicadores do IBGE;
- recuperação dos textos coletados por categoria;
- funcionamento do mecanismo de contingência;
- retorno HTTP 200 nas solicitações válidas testadas;
- retorno HTTP 503 quando o modelo local está indisponível.

Também foram identificadas limitações nas respostas do modelo, incluindo extrapolações, respostas incompletas e dificuldades na interpretação dos textos.

Nos testes de sumarização, algumas categorias utilizaram a saída alternativa. Na categoria Obstáculos, a resposta do LLM apresentou informações não sustentadas pelas evidências, apesar de ter passado pela verificação automática.

O modelo é utilizado como ferramenta complementar, e seus resultados devem ser conferidos com as fontes originais.

### Ambiente de testes

- Windows;
- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- Intel Core i7-1260P;
- aproximadamente 15,6 GB de memória RAM;
- execução em CPU.

Em um teste com geração de até 80 novos tokens, foram observados os tempos de 9,48 segundos na primeira geração e 8,44 segundos na segunda.

Esses tempos correspondem ao ambiente e às condições específicas do teste realizado.

## 16. ESG e ODS 11

O projeto está relacionado ao ODS 11 — Cidades e Comunidades Sustentáveis.

A análise de indicadores de acessibilidade urbana, mobilidade e condições das calçadas pode contribuir para estudos relacionados à inclusão social e ao planejamento urbano.

No contexto acadêmico, a proposta está associada principalmente à dimensão Social do ESG.

A aplicação não substitui avaliações técnicas de acessibilidade ou diagnósticos realizados diretamente nos locais analisados.

## 17. Documentação do projeto

### Entendimento do negócio

- [Project Charter](01_business_understanding/project_charter.md)

### Aquisição e entendimento dos dados

- [Data Summary Report](02_data_acquisition_understanding/data_summary_report.md)

### Modelagem

- [Modeling Report](03_modeling/modeling_report.md)
- [Escolha do modelo](03_modeling/escolha_modelo.md)
- [Integração do LLM](03_modeling/integracao_llm.md)
- [Engenharia de Prompt](03_modeling/prompt_engineering.md)

### Implantação

- [Deployment Report](04_deployment/deployment_report.md)

### Aceitação

- [Customer Acceptance Report](05_customer_acceptance/acceptance_report.md)

## 18. Limitações

A aplicação possui características de um protótipo acadêmico.

O modelo de linguagem utilizado apresenta limitações de interpretação e geração textual.

As fontes de dados possuem diferentes metodologias, períodos e abrangências.

A execução da arquitetura completa foi realizada localmente, sem implantação pública em um servidor externo.

## 19. Autor

Diego Favretto

Curso: Ciência de Dados

Disciplina: Projeto de Bloco — Inteligência Artificial Aplicada

Repositório:

https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil