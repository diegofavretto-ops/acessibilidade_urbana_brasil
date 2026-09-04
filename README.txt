# Acessibilidade Urbana no Brasil

Projeto desenvolvido para o TP1 da disciplina de Projeto de Bloco.

## Sobre o projeto

O projeto tem como objetivo apresentar dados sobre as condições
do entorno urbano nos estados brasileiros, com foco na acessibilidade
das calçadas e no conforto do pedestre durante a caminhada.

São utilizados dados sobre calçadas, obstáculos, rampas, arborização
e outras características do espaço urbano.

## ODS relacionado

ODS 11 - Cidades e Comunidades Sustentáveis.

## Fonte dos dados

Os dados utilizados são provenientes do:

- IBGE
- Censo Demográfico 2022
- Características Urbanísticas do Entorno dos Domicílios
- Tabela SIDRA 9584

Os dados foram inicialmente obtidos em formato XLSX e organizados
em um arquivo CSV para utilização na aplicação.

## Estrutura do projeto

01_business_understanding/
- Contém o Project Charter.

02_data_acquisition_understanding/
- Contém o Data Summary Report.
- Contém o arquivo CSV utilizado pela aplicação.

03_modeling/
- Pasta reservada para etapas futuras de modelagem.

04_deployment/
- Pasta relacionada à implantação da aplicação.

05_customer_acceptance/
- Pasta relacionada à avaliação e aceitação da solução.

app.py
- Código principal da aplicação Streamlit.

requirements.txt
- Bibliotecas necessárias para executar o projeto.

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit

## Como instalar

Crie e ative um ambiente virtual.

No Windows:

python -m venv .venv

.\.venv\Scripts\Activate.ps1

Depois instale as dependências:

pip install -r requirements.txt

## Como executar

Com o ambiente virtual ativado, execute:

streamlit run app.py

A aplicação será aberta no navegador.

## Dados utilizados

A aplicação utiliza o arquivo:

02_data_acquisition_understanding/ufs_streamlit_resumo.csv

Os indicadores estão apresentados em percentuais para facilitar
a visualização e comparação entre as Unidades da Federação.

## Uso de Inteligência Artificial

Foi utilizada a ferramenta ChatGPT como apoio no desenvolvimento
da aplicação Streamlit, conforme permitido para a etapa de programação
do projeto.

Para instalar as dependências:

pip install -r requirements.txt

Para executar o Web Scraping:

python 02_data_acquisition_understanding/scraping_mobilize.py

Para executar a aplicação:

streamlit run app.py