# Data Summary Report

## 1. Fonte quantitativa principal

A principal fonte quantitativa utilizada no projeto é:

**IBGE - Censo Demográfico 2022 - Características Urbanísticas do Entorno dos Domicílios - Tabela SIDRA 9584.**

Os dados foram organizados por Unidade da Federação para utilização no
dashboard, na API e na geração de resumos com o modelo de linguagem local.

## 2. Dados do IBGE utilizados

Os principais campos da base são:

| Campo | Tipo | Objetivo |
|---|---|---|
| Estado | String | Identificar a Unidade da Federação |
| Regiao | String | Identificar a região brasileira |
| Domicilios_base | Integer | Quantidade de domicílios utilizada como referência |
| Iluminacao_publica_pct | Float | Presença de iluminação pública no entorno |
| Ponto_onibus_van_pct | Float | Presença de ponto de ônibus ou van |
| Via_bicicleta_pct | Float | Presença de infraestrutura para bicicleta |
| Calcada_passeio_pct | Float | Presença de calçada ou passeio |
| Calcadas_sem_obstaculos_pct | Float | Calçadas sem obstáculos |
| Rampas_pct | Float | Presença de rampas |
| Arborizacao_com_arvores_pct | Float | Presença de arborização |

Os percentuais representam características observadas no entorno dos domicílios
considerados na pesquisa.

Por isso, os valores não devem ser interpretados diretamente como percentual de
todas as ruas existentes em cada Unidade da Federação.

Também é importante considerar que os indicadores de rampas e calçadas sem
obstáculos possuem contexto metodológico relacionado aos locais onde existe
calçada.

O projeto não utiliza esses indicadores como uma certificação geral de
acessibilidade de uma UF.

## 3. Primeira fonte complementar por Web Scraping

Como fonte complementar foi utilizado o levantamento do Mobilize Brasil:

**Calçadas do Brasil: notas em 228 locais.**

A coleta é realizada pelo script:

`02_data_acquisition_understanding/scraping_mobilize.py`

O script utiliza:

- Requests;
- BeautifulSoup;
- Pandas.

A página possui avaliações de locais segundo diferentes critérios relacionados
às condições das calçadas.

### Campos coletados

| Campo | Tipo | Objetivo |
|---|---|---|
| Endereco | String | Identificar o local avaliado |
| Cidade | String | Cidade ou localidade |
| Irregularidades | Float | Nota relacionada às irregularidades do piso |
| Degraus | Float | Nota relacionada à presença de degraus |
| Inclinacao | Float | Nota relacionada à inclinação |
| Largura | Float | Nota relacionada à largura |
| Rampas | Float | Nota relacionada às rampas |
| Obstaculos | Float | Nota relacionada aos obstáculos |
| Iluminacao | Float | Nota relacionada à iluminação |
| Arborizacao | Float | Nota relacionada à arborização |
| Sinalizacao | Float | Nota relacionada à sinalização |
| Media | Float | Nota média do local |

As notas do Mobilize são apresentadas em uma escala de 0 a 10 e não devem ser
comparadas diretamente com os percentuais do IBGE.

Os arquivos gerados são:

- `data/calcadas_mobilize.csv`;
- `data/calcadas_mobilize.txt`;
- `data/texto_mobilize.txt`.

## 4. Segunda página coletada por Web Scraping

Para ampliar a utilização de Web Scraping no projeto foi adicionada uma segunda
página do Mobilize Brasil:

**Panorama das calçadas.**

A coleta é realizada pelo script:

`02_data_acquisition_understanding/scraping_mobilize_panorama.py`

Essa coleta possui uma estrutura diferente da primeira.

Na primeira página o objetivo é extrair uma tabela com dados numéricos.

Na segunda página o objetivo é analisar parágrafos e itens de texto relacionados
aos critérios utilizados no estudo das calçadas.

Os textos são classificados segundo categorias como:

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

Durante a coleta válida realizada no desenvolvimento do TP4 foram obtidos 17
trechos relacionados a esses temas.

Os resultados são armazenados em:

- `data/mobilize_panorama_calcadas.csv`;
- `data/mobilize_panorama_calcadas.txt`.

Na aplicação Streamlit esses dados podem ser filtrados por categoria e também
são apresentados em tabela e gráfico de frequência.

## 5. Tratamento da indisponibilidade da fonte externa

Durante o desenvolvimento foi observado que o site Mobilize pode responder com
código HTTP 200 e, mesmo assim, apresentar internamente a mensagem:

`Esta página não pode ser exibida no momento`

Nesse caso, o código HTTP sozinho não é suficiente para considerar a coleta
bem-sucedida.

Os dois scripts de Web Scraping foram adaptados para verificar também o conteúdo
recebido.

Quando a página está disponível, o processo realiza a coleta normalmente.

Quando a página apresenta a mensagem de indisponibilidade, o script:

1. identifica a falha da fonte;
2. não sobrescreve os dados existentes;
3. verifica se existe um último snapshot válido;
4. mantém os arquivos anteriormente coletados;
5. informa a situação no terminal sem gerar um traceback desnecessário.

No momento da validação dessa contingência foram preservados:

- 228 registros da tabela de avaliações;
- 17 trechos da página Panorama das Calçadas.

Essa estratégia evita que uma indisponibilidade temporária de uma fonte externa
destrua dados válidos previamente coletados.

## 6. Visualização de frequência de termos

Para atender ao feedback recebido em etapa anterior do projeto, foi implementada
uma visualização de frequência de termos.

O arquivo:

`data/texto_mobilize.txt`

é construído utilizando os campos textuais obtidos na primeira raspagem.

A aplicação utiliza `Counter`, da biblioteca padrão do Python, para contar os
termos mais frequentes.

Palavras pouco informativas são removidas e os termos restantes são apresentados
em:

- tabela;
- gráfico de barras.

A segunda fonte também possui uma visualização da frequência das categorias
identificadas nos 17 trechos coletados.

## 7. Relação entre IBGE e Mobilize

IBGE e Mobilize possuem alguns temas semelhantes, como:

- rampas;
- obstáculos;
- iluminação;
- arborização;
- condições das calçadas.

Entretanto, as duas fontes possuem:

- metodologias diferentes;
- períodos diferentes;
- unidades de análise diferentes;
- escalas diferentes.

Por isso, os valores não são comparados numericamente de forma direta.

O Mobilize é utilizado como referência complementar ao conjunto de dados
principal do IBGE.

## 8. Decisão sobre Selenium

Selenium foi avaliado durante o desenvolvimento.

Para as fontes selecionadas, não foi necessário utilizar automação de navegador
porque os dados de interesse podem ser obtidos do HTML utilizando Requests e
BeautifulSoup quando as páginas estão disponíveis.

Por isso, o projeto mantém a solução mais simples.

Quando a fonte externa está temporariamente indisponível, o projeto preserva o
último snapshot válido em vez de utilizar Selenium apenas para tentar contornar
a indisponibilidade do servidor.

## 9. API FastAPI

A aplicação possui uma API desenvolvida com FastAPI.

A API disponibiliza os dados existentes em um formato que pode ser consumido
por outros programas.

As principais rotas relacionadas aos dados são:

- `GET /`;
- `GET /ufs`;
- `GET /ufs/{estado}`;
- `POST /observacoes`;
- `GET /observacoes`.

No TP4 foram acrescentadas:

- `GET /ia/status`;
- `POST /ia/resumo-uf`.

## 10. Response Models

As respostas das rotas da FastAPI são estruturadas utilizando modelos Pydantic.

Isso permite validar o formato das respostas e definir de forma explícita quais
campos devem ser devolvidos pela API.

A rota:

`POST /ia/resumo-uf`

utiliza um Response Model contendo:

- estado;
- região;
- modelo utilizado;
- dispositivo de execução;
- indicadores enviados ao modelo;
- resumo produzido pelo LLM.

## 11. Integração com modelo de linguagem local

No TP4 foi integrado o modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente utilizando:

- PyTorch;
- Hugging Face Transformers;
- Hugging Face Hub.

No ambiente utilizado durante o desenvolvimento foram verificados:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA não disponível.

Os arquivos do modelo são armazenados localmente em:

`models/qwen2.5-0.5b-instruct`

A pasta `models/` é ignorada pelo Git e os pesos do modelo não são enviados ao
GitHub.

## 12. Utilização dos dados pelo LLM

O modelo não funciona como um chatbot genérico dentro do projeto.

O usuário seleciona uma Unidade da Federação.

A FastAPI consulta os dados correspondentes e fornece ao modelo os seguintes
indicadores:

- calçada/passeio;
- calçadas sem obstáculos;
- rampas;
- arborização.

O prompt orienta o modelo a:

- utilizar somente os dados fornecidos;
- não inventar valores;
- não utilizar informações externas;
- não classificar uma UF como acessível ou inacessível;
- não interpretar os valores como percentual de todas as ruas;
- não criar um índice geral de acessibilidade;
- produzir um resumo curto em português do Brasil.

## 13. Tratamento de erros da API

A integração com o modelo possui tratamento de diferentes situações.

### HTTP 404

Utilizado quando a Unidade da Federação solicitada não existe na base.

### HTTP 422

Utilizado quando os dados de entrada não passam pela validação realizada pelo
Pydantic.

### HTTP 503

Utilizado quando os arquivos do modelo local não estão disponíveis ou quando o
modelo não pode ser carregado ou executado.

### HTTP 500

Utilizado para uma falha inesperada durante a geração da resposta.

Esses comportamentos foram testados durante o desenvolvimento do TP4.

## 14. Integração com Streamlit

A página:

`pages/api_llm.py`

consome as respostas da FastAPI.

Diferentemente da versão anterior do projeto, os resultados da API não são
apresentados somente como JSON.

Eles são utilizados para alimentar:

- tabela de indicadores;
- gráfico de barras;
- informações sobre o modelo;
- resumo textual produzido pelo Qwen.

O fluxo principal é:

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
Qwen local
    ↓
Response Model
    ↓
Streamlit
    ├── tabela
    ├── gráfico
    └── resumo