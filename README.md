## Acessibilidade Urbana no Brasil

Projeto desenvolvido na disciplina de **Projeto de Bloco - Inteligência Artificial
Aplicada**.

## Etapa atual

**TP4**

## Objetivo

Organizar, visualizar e comparar dados relacionados à acessibilidade urbana no
Brasil utilizando Python, Pandas, Streamlit, Web Scraping, FastAPI e um modelo
de linguagem executado localmente.

O projeto está relacionado ao **ODS 11 - Cidades e Comunidades Sustentáveis**.

## Evolução do projeto

O projeto foi desenvolvido de forma incremental ao longo dos TPs.

No TP3 foram implementados:

- aplicação Streamlit com múltiplas páginas;
- visualização de frequência de termos;
- API com FastAPI;
- rotas para consulta das UFs;
- registro de observações;
- preparação para futura integração com modelos de linguagem.

No TP4 foram acrescentados:

- uma segunda página coletada por Web Scraping;
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

Os percentuais representam características observadas no entorno dos domicílios
considerados na pesquisa e não devem ser interpretados diretamente como
percentual de todas as ruas de cada UF.

### Mobilize Brasil

O projeto utiliza duas páginas do Mobilize Brasil como fontes complementares
obtidas por Web Scraping.

A primeira é o levantamento:

`Calçadas do Brasil: notas em 228 locais`

Essa página fornece avaliações numéricas relacionadas às condições das calçadas.

A segunda é a página:

`Panorama das calçadas`

Essa página é utilizada para coleta de trechos textuais relacionados a temas
como:

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

A primeira realiza a extração de uma tabela HTML.

A segunda analisa parágrafos e itens de texto.

## Selenium

Selenium foi avaliado, mas não foi necessário para as fontes utilizadas.

Os dados necessários estão disponíveis diretamente no HTML e podem ser coletados
com Requests e BeautifulSoup.

Essa decisão mantém a solução mais simples e evita utilizar uma ferramenta de
automação de navegador quando ela não é necessária.

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
│
├── data/
│
└── models/
    └── qwen2.5-0.5b-instruct/