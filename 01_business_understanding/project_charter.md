# Project Charter

## Nome do projeto

Acessibilidade Urbana no Brasil


## Problema

As condições de infraestrutura do entorno urbano não são iguais em todo o Brasil. 
Elementos como a existência de calçadas, a presença de rampas, obstáculos nos 
passeios e arborização podem influenciar a acessibilidade e o conforto dos 
pedestres durante seus deslocamentos.

Essas características são especialmente importantes para pessoas com mobilidade 
reduzida, idosos e demais usuários que dependem de condições adequadas para se 
deslocar a pé com segurança e autonomia.

O IBGE disponibiliza dados sobre essas características por meio do Censo 
Demográfico 2022. Entretanto, essas informações estão organizadas em grandes 
tabelas estatísticas, o que pode dificultar sua interpretação e comparação.

O projeto busca facilitar a visualização e a consulta desses dados por meio de 
uma aplicação desenvolvida em Streamlit.


## Objetivo geral

Desenvolver uma aplicação em Streamlit que facilite a consulta e a comparação 
de indicadores relacionados à acessibilidade das calçadas e às condições de 
conforto do pedestre nas Unidades da Federação brasileiras.


## Objetivos específicos

- Organizar os dados do Censo Demográfico 2022 do IBGE relacionados às 
  características do entorno dos domicílios.

- Apresentar os dados de forma simplificada e compreensível.

- Permitir a consulta dos indicadores por região e Unidade da Federação.

- Destacar indicadores relacionados à existência de calçadas, obstáculos, 
  rampas e arborização.

- Utilizar conteúdo complementar obtido de iniciativas relacionadas à 
  acessibilidade urbana.

- Permitir que o usuário interaja com os dados através da aplicação Streamlit.


## Metas

### Meta 1

Disponibilizar dados das 27 Unidades da Federação brasileiras, correspondendo 
a 100% das UFs presentes na base utilizada pelo projeto.


### Meta 2

Disponibilizar os quatro indicadores principais do projeto — existência de 
calçada/passeio, calçadas sem obstáculos, presença de rampas e arborização — 
para todas as Unidades da Federação, buscando 100% de completude dos registros 
utilizados.


### Meta 3

Apresentar 100% dos quatro indicadores principais em formato percentual, 
permitindo sua comparação entre as Unidades da Federação.


## Indicadores de sucesso

| Indicador | Resultado esperado |
|---|---|
| Unidades da Federação disponíveis | 27 de 27 UFs (100%) |
| Completude dos quatro indicadores principais | 100% dos registros utilizados |
| Indicadores principais apresentados em percentual | 4 de 4 indicadores (100%) |


## Escopo

O projeto utiliza dados das 27 Unidades da Federação brasileiras provenientes 
do Censo Demográfico 2022 do IBGE, principalmente das informações sobre 
Características Urbanísticas do Entorno dos Domicílios.

O foco principal está nos indicadores relacionados às condições de circulação 
e conforto dos pedestres:

- existência de calçada ou passeio;
- presença ou ausência de obstáculos nas calçadas;
- existência de rampas para cadeirantes;
- arborização no entorno dos domicílios.

Outros indicadores existentes na base, como iluminação pública, ponto de 
ônibus ou van e infraestrutura para bicicletas, poderão ser utilizados como 
informações complementares.

No TP2, o projeto também utilizará conteúdo textual obtido através de Web 
Scraping de iniciativas relacionadas à acessibilidade e à qualificação das 
calçadas.

A aplicação será desenvolvida utilizando Python, Pandas e Streamlit.


## Fora do escopo

O projeto não pretende realizar uma avaliação técnica individual das calçadas 
de cada município ou rua.

Os indicadores apresentados não representam uma certificação de atendimento 
às normas técnicas de acessibilidade, como a ABNT NBR 9050.

Também não será realizada, nesta etapa, modelagem preditiva ou utilização de 
Machine Learning.

A análise será realizada no nível das Unidades da Federação, não sendo objetivo 
desta etapa avaliar individualmente todos os municípios brasileiros.


## Funcionalidades da aplicação

A aplicação deverá possuir as seguintes funcionalidades:

- apresentação do objetivo e do problema do projeto;

- seleção de uma ou mais regiões brasileiras;

- seleção de uma Unidade da Federação;

- seleção dos indicadores que o usuário deseja consultar;

- apresentação dos valores dos indicadores selecionados;

- visualização de uma tabela com os dados;

- apresentação de informações complementares obtidas através de Web Scraping;

- utilização de cache para evitar carregamentos desnecessários dos dados;

- utilização de estado de sessão para manter informações durante a interação 
  do usuário;

- possibilidade de upload de arquivos CSV com dados complementares;

- possibilidade de download dos dados filtrados em formato CSV;

- apresentação das fontes de dados utilizadas;

- apresentação de iniciativas relacionadas ao tema do projeto;

- apresentação da relação do projeto com o ODS 11 da Agenda 2030.


## Público-alvo

O projeto poderá ser utilizado por:

- cidadãos interessados em conhecer as condições do entorno urbano;

- estudantes e pesquisadores;

- engenheiros;

- arquitetos e urbanistas;

- profissionais que trabalham com planejamento urbano;

- gestores públicos;

- pessoas interessadas em acessibilidade e mobilidade urbana.


## Stakeholders

Os principais stakeholders identificados são:

### Usuários da aplicação

Pessoas que utilizarão a aplicação para consultar e comparar os indicadores 
urbanos apresentados.


### Gestores públicos

Profissionais que podem utilizar os indicadores como fonte complementar para 
compreender diferenças existentes entre as Unidades da Federação.


### Engenheiros, arquitetos e urbanistas

Profissionais relacionados ao planejamento, projeto e análise dos espaços 
urbanos.


### Estudantes e pesquisadores

Usuários que podem utilizar a aplicação como ferramenta para consulta e 
visualização dos dados.


### IBGE

Instituição responsável pela produção e disponibilização dos dados utilizados 
como principal fonte quantitativa do projeto.


### Desenvolvedor do projeto

Responsável pela organização dos dados, desenvolvimento da aplicação, 
documentação e manutenção do projeto.


## Fontes de dados

A principal fonte de dados quantitativos do projeto é:

- IBGE - Instituto Brasileiro de Geografia e Estatística;
- Censo Demográfico 2022;
- Características Urbanísticas do Entorno dos Domicílios;
- Sistema SIDRA;
- Tabela SIDRA 9584.

No TP2 também será utilizado conteúdo complementar obtido através de Web 
Scraping de páginas relacionadas a iniciativas de acessibilidade urbana.


## Iniciativas relacionadas

Como referências e iniciativas semelhantes ao tema do projeto serão 
considerados programas relacionados à melhoria das condições de circulação 
dos pedestres e acessibilidade das calçadas, entre eles:

- Programa Calçada Certa - Florianópolis;
- Programa Rotas Acessíveis - Florianópolis;
- Programa Calçada Segura - Cascavel.

Essas iniciativas são utilizadas como referência para compreender formas de 
abordar aspectos como acessibilidade, circulação de pedestres, obstáculos, 
qualificação das calçadas e conforto no espaço urbano.


## ODS relacionado

O projeto está relacionado ao:

**ODS 11 - Cidades e Comunidades Sustentáveis.**

O ODS 11 busca tornar as cidades e os assentamentos humanos mais inclusivos, 
seguros, resilientes e sustentáveis.

O projeto se relaciona com esse objetivo porque analisa características do 
entorno urbano que interferem na circulação dos pedestres e na acessibilidade 
dos espaços urbanos, como a existência de calçadas, rampas, obstáculos e 
arborização.


## Tecnologias utilizadas

As principais tecnologias previstas para o projeto são:

- Python;
- Pandas;
- Streamlit;
- Requests;
- BeautifulSoup;
- Git;
- GitHub.


## Metodologia

O projeto será organizado seguindo as fases do TDSP - Team Data Science Process:

1. Business Understanding;
2. Data Acquisition and Understanding;
3. Modeling;
4. Deployment;
5. Customer Acceptance.

No TP2, o projeto avança principalmente nas etapas de aquisição e entendimento 
dos dados, desenvolvimento da aplicação, preparação para deployment e testes 
da solução.