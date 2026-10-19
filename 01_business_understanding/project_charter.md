# Project Charter

## Nome do projeto

Acessibilidade Urbana no Brasil

## Problema de negócio

Dados de acessibilidade e características do entorno urbano podem ser difíceis
de consultar e comparar quando estão distribuídos em tabelas e fontes distintas.
O projeto busca organizar essas informações em uma aplicação simples, permitindo
que diferentes usuários consultem indicadores e façam comparações entre Unidades
da Federação e regiões brasileiras.

## Objetivo

Desenvolver uma aplicação multipágina em Streamlit para facilitar a visualização,
consulta e comparação de dados relacionados à acessibilidade e ao conforto do
pedestre no entorno urbano.

No TP3, o projeto também disponibiliza parte das informações por meio de uma API
construída com FastAPI e organiza a arquitetura para futura integração com modelos
de linguagem (LLMs).

## Escopo

A base quantitativa principal utiliza dados das 27 Unidades da Federação do
Censo Demográfico 2022 do IBGE, relacionados às Características Urbanísticas
do Entorno dos Domicílios.

### Indicadores principais

- existência de calçada ou passeio;
- calçadas sem obstáculos;
- rampas;
- arborização.

### Indicadores complementares

- iluminação pública;
- ponto de ônibus ou van;
- infraestrutura para bicicleta.

### Evoluções implementadas no TP3

- reorganização do Streamlit em múltiplas páginas;
- menu de navegação com `st.Page` e `st.navigation`;
- separação de funções compartilhadas em `comum.py`;
- manutenção do Web Scraping com Requests e BeautifulSoup;
- gráfico de frequência de termos coletados no scraping;
- API em FastAPI com rotas GET e POST;
- integração local entre Streamlit e FastAPI;
- preparação documental para futura integração com LLMs;
- reorganização do repositório para manter apenas uma versão atual do projeto.

## Decisão sobre Selenium

A necessidade de Selenium foi avaliada. A fonte complementar atualmente utilizada
permite acessar a tabela necessária diretamente no HTML, sem cliques, formulários
ou carregamento assíncrono obrigatório. Por isso, manteve-se Requests e
BeautifulSoup, evitando complexidade desnecessária.

Selenium poderá ser incorporado futuramente caso seja adotada uma fonte que exija
interação dinâmica.

## Preparação para LLM

As possibilidades priorizadas para a próxima etapa são:

1. perguntas e respostas baseadas nos indicadores disponíveis;
2. geração automática de relatórios e resumos de uma UF ou região.

A classificação de sentimentos não foi priorizada, pois as principais fontes
atuais são dados estatísticos e técnicos, e não opiniões de usuários.

## Stakeholders

- gestores públicos;
- engenheiros;
- arquitetos e urbanistas;
- estudantes;
- pesquisadores;
- cidadãos interessados em acessibilidade, mobilidade e qualidade do espaço urbano.

## ODS relacionado

ODS 11 - Cidades e Comunidades Sustentáveis.
