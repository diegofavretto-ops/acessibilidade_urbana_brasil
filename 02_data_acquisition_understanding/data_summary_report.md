# Data Summary Report

## Fonte

IBGE - Censo Demográfico 2022
Características Urbanísticas do Entorno dos Domicílios.

## Dados utilizados

| Campo | Tipo | Objetivo |
|---|---|---|
| Estado | String | Identificar a Unidade da Federação |
| Região | String | Identificar a região brasileira |
| Domicílios base | Integer | Informar a quantidade de domicílios utilizada como referência |
| Iluminação pública (%) | Float | Analisar presença de iluminação no entorno |
| Ponto de ônibus/van (%) | Float | Analisar infraestrutura de transporte |
| Via para bicicleta (%) | Float | Analisar infraestrutura cicloviária |
| Calçada/passeio (%) | Float | Analisar presença de calçadas |
| Calçadas sem obstáculos (%) | Float | Analisar condições de circulação |
| Rampas (%) | Float | Analisar presença de rampas |
| Arborização (%) | Float | Analisar presença de arborização no entorno |

## Fonte complementar obtida por Web Scraping

Como fonte complementar será utilizada a página
"Calçadas do Brasil: notas em 228 locais", publicada pelo Mobilize Brasil.

A página apresenta avaliações realizadas em diferentes locais do Brasil
e utiliza critérios relacionados à qualidade das calçadas.

Os dados serão coletados utilizando Requests e BeautifulSoup e serão
armazenados em arquivos CSV e TXT dentro da pasta data/.

### Campos coletados

| Campo | Tipo | Objetivo |
|---|---|---|
| Endereco | String | Identificar o local avaliado |
| Irregularidades | Float | Nota relacionada às irregularidades |
| Degraus | Float | Nota relacionada à presença de degraus |
| Inclinacao | Float | Nota relacionada à inclinação |
| Largura | Float | Nota relacionada à largura |
| Rampas | Float | Nota relacionada às rampas |
| Obstaculos | Float | Nota relacionada aos obstáculos |
| Iluminacao | Float | Nota relacionada à iluminação |
| Arborizacao | Float | Nota relacionada à arborização |
| Sinalizacao | Float | Nota relacionada à sinalização |
| Media | Float | Média da avaliação do local |

## Relação com os dados do IBGE

Alguns critérios utilizados pelo Mobilize possuem relação temática
com indicadores existentes na base do IBGE, principalmente:

- rampas;
- obstáculos;
- iluminação;
- arborização.

Entretanto, as duas bases possuem metodologias, períodos, unidades de
análise e escalas diferentes.

Por esse motivo, os valores do Mobilize serão utilizados apenas como
referência complementar e não serão comparados numericamente de forma
direta com os percentuais do IBGE.

## Dados complementares enviados pelo usuário

A aplicação também permitirá o upload de arquivos CSV.

Para permitir a integração com a base principal, o arquivo deverá
possuir uma coluna chamada Estado.

As demais colunas poderão conter informações complementares relacionadas
às Unidades da Federação.