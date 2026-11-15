# Data Summary Report

## 1. Fonte quantitativa principal

IBGE - Censo Demográfico 2022 - Características Urbanísticas do Entorno dos
Domicílios - Tabela SIDRA 9584.

## 2. Dados do IBGE utilizados

| Campo | Tipo | Objetivo |
|---|---|---|
| Estado | String | Identificar a Unidade da Federação |
| Regiao | String | Identificar a região brasileira |
| Domicilios_base | Integer | Quantidade de domicílios utilizada como referência |
| Iluminacao_publica_pct | Float | Presença de iluminação no entorno |
| Ponto_onibus_van_pct | Float | Infraestrutura de transporte |
| Via_bicicleta_pct | Float | Infraestrutura cicloviária |
| Calcada_passeio_pct | Float | Presença de calçada/passeio |
| Calcadas_sem_obstaculos_pct | Float | Condições de circulação |
| Rampas_pct | Float | Presença de rampas |
| Arborizacao_com_arvores_pct | Float | Arborização do entorno |

Os percentuais se referem às características observadas no entorno dos domicílios
considerados no levantamento e não devem ser interpretados diretamente como
percentual de todas as ruas de cada UF.

## 3. Fonte complementar por Web Scraping

Como fonte complementar é utilizada a página "Calçadas do Brasil: notas em 228
locais", publicada pelo Mobilize Brasil.

A coleta é realizada em um script separado utilizando Requests e BeautifulSoup.
A tabela coletada é armazenada em `data/calcadas_mobilize.csv` e
`data/calcadas_mobilize.txt`.

### Campos coletados

| Campo | Tipo | Objetivo |
|---|---|---|
| Endereco | String | Identificar o local avaliado |
| Cidade | String | Cidade/localidade extraída do texto da fonte |
| Irregularidades | Float | Nota relacionada às irregularidades do piso |
| Degraus | Float | Nota relacionada à presença de degraus |
| Inclinacao | Float | Nota relacionada à inclinação |
| Largura | Float | Nota relacionada à largura |
| Rampas | Float | Nota relacionada às rampas |
| Obstaculos | Float | Nota relacionada aos obstáculos |
| Iluminacao | Float | Nota relacionada à iluminação |
| Arborizacao | Float | Nota relacionada à arborização |
| Sinalizacao | Float | Nota relacionada à sinalização |
| Media | Float | Média da avaliação do local |

As notas do Mobilize variam de 0 a 10 e não são percentuais.

## 3.1 Segunda página coletada por Web Scraping

Como complemento à tabela de avaliações, também é utilizada a página
"Panorama das calçadas", do Mobilize Brasil.

Essa segunda coleta utiliza Requests e BeautifulSoup, mas possui uma estrutura
diferente da primeira fonte. Em vez de extrair uma tabela, o script analisa
parágrafos e itens de texto da página.

Os trechos são classificados conforme termos relacionados ao projeto, incluindo:

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

Na execução realizada durante o TP4 foram coletados 17 trechos relacionados a
esses temas.

Os resultados são armazenados em:

- `data/mobilize_panorama_calcadas.csv`;
- `data/mobilize_panorama_calcadas.txt`.

Na aplicação Streamlit, esses dados são apresentados com filtro por categoria,
tabela dos trechos encontrados e gráfico de frequência das categorias.

## 4. Visualização de frequência de termos

Para corrigir a ausência apontada na avaliação do TP2, o processo de scraping
também gera `data/texto_mobilize.txt`, construído com os campos textuais de
endereço e cidade/localidade coletados na tabela.

A aplicação utiliza esse conteúdo para contar termos com `Counter`, filtrar
palavras pouco informativas e apresentar um gráfico de frequência com
`st.bar_chart`.

## 5. Relação entre IBGE e Mobilize

Alguns critérios possuem relação temática, principalmente rampas, obstáculos,
iluminação e arborização. Entretanto, as bases possuem metodologias, períodos,
unidades de análise e escalas diferentes.

Por isso, as notas do Mobilize são apresentadas somente como referência
complementar e não são comparadas numericamente de forma direta com os
percentuais do IBGE.

## 6. Decisão sobre Selenium

Selenium foi avaliado, mas não foi necessário para a fonte atual. Os dados
necessários estão disponíveis diretamente no HTML e podem ser coletados com
Requests e BeautifulSoup.

Essa decisão mantém o projeto simples e evita executar no aplicativo uma coleta
mais custosa sem necessidade.

## 7. API FastAPI

A API não cria uma nova fonte de dados. Ela disponibiliza os dados existentes em
formato apropriado para consumo por programas.

Rotas principais:

- `GET /ufs`: lista as 27 UFs;
- `GET /ufs/{estado}`: consulta uma UF específica;
- `POST /observacoes`: registra uma observação complementar;
- `GET /observacoes`: lista observações registradas.

As observações são armazenadas localmente em `data/observacoes_api.csv`, arquivo
gerado em tempo de execução.

## 8. Dados complementares enviados pelo usuário

O Streamlit permite upload de CSV. O arquivo precisa possuir a coluna `Estado`.
As demais colunas são incorporadas à base por meio de `merge`, mantendo todas as
UFs da base principal.

## 9. Preparação para LLM

Os dados estruturados do IBGE, as avaliações do Mobilize e as observações da API
podem futuramente ser fornecidos a um LLM para perguntas e respostas e geração
de relatórios textuais baseados nos dados disponíveis.
