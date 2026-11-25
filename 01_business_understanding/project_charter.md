# Project Charter

## Nome do projeto

**Acessibilidade Urbana no Brasil**

## Problema

Dados relacionados à acessibilidade urbana, mobilidade de pedestres e características do entorno podem estar distribuídos em diferentes fontes e formatos, dificultando sua consulta, comparação e interpretação.

O projeto busca organizar dados públicos e informações complementares em uma aplicação única, permitindo consultar indicadores urbanos, comparar Unidades da Federação e regiões e analisar conteúdos relacionados às condições das calçadas.

A proposta não é classificar uma cidade ou Unidade da Federação como simplesmente acessível ou inacessível, mas facilitar a leitura de indicadores e evidências disponíveis.

## Objetivo

Desenvolver uma aplicação de Ciência de Dados que integre coleta, tratamento, análise, visualização e Inteligência Artificial para apoiar a interpretação de dados relacionados à acessibilidade urbana no Brasil.

A solução utiliza:

- dados do Censo Demográfico 2022 do IBGE;
- Web Scraping de informações do Mobilize Brasil;
- tratamento e análise com Python e Pandas;
- dashboard multipágina desenvolvido com Streamlit;
- API desenvolvida com FastAPI;
- modelo de linguagem executado localmente;
- Engenharia de Prompt para controlar as respostas do modelo;
- validação das respostas geradas pela IA.

## Relação com o problema de negócio

A principal contribuição do projeto é transformar dados originalmente distribuídos em tabelas e páginas da internet em informações mais fáceis de consultar.

O usuário pode visualizar indicadores, realizar comparações, consultar dados complementares sobre calçadas e utilizar a Inteligência Artificial para apoiar a síntese de conteúdos textuais coletados por Web Scraping.

Dessa forma, a aplicação procura reduzir o esforço necessário para localizar e interpretar as informações utilizadas no projeto.

## Escopo dos dados

### Fonte quantitativa principal

A base principal utiliza dados do:

**IBGE — Censo Demográfico 2022 — Características Urbanísticas do Entorno dos Domicílios — Tabela SIDRA 9584.**

Os dados foram organizados para as 27 Unidades da Federação.

Os principais indicadores utilizados são:

- existência de calçada ou passeio;
- calçadas sem obstáculos;
- presença de rampas;
- arborização com árvores;
- iluminação pública;
- ponto de ônibus ou van;
- infraestrutura para bicicleta.

Os percentuais representam características observadas no entorno dos domicílios considerados pelo IBGE e não devem ser interpretados como percentual de todas as ruas de uma Unidade da Federação.

### Fontes complementares

O projeto também utiliza duas páginas do Mobilize Brasil obtidas por Web Scraping:

- **Calçadas do Brasil: notas em 228 locais**;
- **Panorama das Calçadas**.

A primeira fonte fornece avaliações numéricas de diferentes características das calçadas.

A segunda fornece conteúdos textuais relacionados a categorias como:

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

As fontes do Mobilize possuem metodologia e unidade de análise diferentes das informações do IBGE e, por isso, são utilizadas de forma complementar, sem comparação numérica direta entre os dois conjuntos.

## Ciclo de Ciência de Dados

O projeto foi organizado de forma a representar um ciclo completo de Ciência de Dados.

### 1. Entendimento do problema

Foi definido o problema relacionado à dificuldade de consulta e interpretação de informações sobre acessibilidade e características urbanas.

### 2. Aquisição e entendimento dos dados

Os dados quantitativos do IBGE foram organizados para utilização na aplicação.

Informações complementares do Mobilize Brasil foram obtidas utilizando Web Scraping com Requests e BeautifulSoup.

### 3. Preparação e análise

Os dados foram tratados com Python e Pandas.

Foram realizadas operações como:

- seleção de indicadores;
- organização por Unidade da Federação;
- cálculo de médias;
- rankings;
- comparação entre UFs e regiões;
- frequência de termos;
- frequência de categorias dos textos coletados.

### 4. Modelagem e Inteligência Artificial

O projeto utiliza o modelo local:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é utilizado para gerar textos a partir de informações reais do projeto.

Uma das funcionalidades utiliza indicadores selecionados do IBGE para produzir uma análise textual curta.

A funcionalidade principal de sumarização utiliza os textos obtidos por Web Scraping do Mobilize.

### 5. Apresentação dos resultados

Os resultados são disponibilizados em uma aplicação multipágina desenvolvida com Streamlit.

A FastAPI funciona como uma camada intermediária para consulta de dados e execução das funcionalidades de IA.

## Funcionalidade de sumarização de textos

A funcionalidade de Inteligência Artificial escolhida para a etapa final do projeto é a **sumarização automatizada de textos**.

O fluxo utilizado é:

```text
Web Scraping
    ↓
textos do Mobilize
    ↓
seleção por categoria
    ↓
FastAPI
    ↓
Engenharia de Prompt
    ↓
Qwen local
    ↓
validação da resposta
    ↓
resultado apresentado no Streamlit
```

O usuário seleciona uma categoria, como `Rampas`, e pode visualizar os textos originais utilizados como evidência antes de solicitar a síntese.

## Engenharia de Prompt

O modelo recebe instruções para reduzir respostas não sustentadas pelos dados.

Entre as restrições utilizadas estão:

- utilizar somente as evidências fornecidas;
- não inventar informações externas;
- não transformar critérios de avaliação em problemas constatados;
- não transformar existência de um item em ausência;
- não produzir recomendações não solicitadas;
- limitar o tamanho da resposta;
- responder em português do Brasil.

Durante os testes foi observado que um modelo pequeno pode continuar realizando extrapolações mesmo quando recebe instruções explícitas.

Por isso, o projeto também implementa uma validação da saída gerada.

## Validação da resposta da IA

A aplicação não apresenta automaticamente qualquer resposta gerada pelo modelo.

A resposta passa por uma verificação para identificar algumas expressões que podem indicar extrapolação das evidências.

Quando necessário, é solicitada uma segunda geração com instruções mais restritivas.

Se a resposta continuar apresentando uma interpretação não sustentada pelos textos, a aplicação utiliza uma síntese de segurança baseada somente nas informações explícitas das evidências.

O dashboard informa ao usuário qual método foi utilizado, evitando apresentar uma síntese de segurança como se fosse uma resposta validada do LLM.

## ODS e ESG

O projeto está relacionado ao:

**ODS 11 — Cidades e Comunidades Sustentáveis.**

Os indicadores analisados estão relacionados à mobilidade, acessibilidade, circulação de pedestres e características do ambiente urbano.

No contexto acadêmico deste projeto, a acessibilidade urbana também possui relação principalmente com a dimensão **Social (S)** do ESG, por envolver condições urbanas que podem influenciar o deslocamento e a utilização dos espaços por diferentes grupos da população.

Essa relação corresponde ao enquadramento utilizado no projeto e não a uma classificação produzida pelas fontes de dados.

## Stakeholders

Os possíveis usuários das informações apresentadas incluem:

- gestores públicos;
- engenheiros;
- arquitetos e urbanistas;
- estudantes;
- pesquisadores;
- cidadãos interessados em mobilidade, acessibilidade e espaço urbano.

## Critérios de sucesso

O projeto será considerado funcional quando:

- os dados das 27 Unidades da Federação puderem ser consultados;
- os principais indicadores puderem ser visualizados e comparados;
- os dados coletados por Web Scraping puderem ser analisados no dashboard;
- os textos originais utilizados pela IA permanecerem disponíveis para conferência;
- a sumarização puder ser solicitada pelo usuário em tempo de execução;
- respostas potencialmente incompatíveis com as evidências sejam identificadas pelo processo de validação;
- a aplicação apresente de forma clara a origem e o método utilizado na síntese;
- o fluxo entre Streamlit, FastAPI, dados e modelo local funcione de maneira integrada.

## Resultado esperado

O resultado final é uma aplicação que reúne dados públicos, coleta de informações da Web, análise exploratória, visualização interativa e Inteligência Artificial em um mesmo fluxo.

O objetivo não é substituir a análise técnica ou produzir uma classificação definitiva de acessibilidade, mas organizar as informações disponíveis e facilitar sua interpretação por meio de uma aplicação de Ciência de Dados.