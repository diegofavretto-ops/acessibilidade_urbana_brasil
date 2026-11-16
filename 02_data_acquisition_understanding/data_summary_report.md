# Data Summary Report

## 1. Fonte quantitativa principal

A principal fonte quantitativa utilizada no projeto é:

**IBGE - Censo Demográfico 2022 - Características Urbanísticas do Entorno dos Domicílios - Tabela SIDRA 9584.**

Os dados foram organizados por Unidade da Federação para utilização no dashboard, na API e na geração de resumos com o modelo de linguagem local.

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

Os percentuais representam características observadas no entorno dos domicílios considerados na pesquisa.

Por isso, os valores não devem ser interpretados diretamente como percentual de todas as ruas existentes em cada Unidade da Federação.

Os indicadores de rampas e calçadas sem obstáculos devem ser interpretados dentro do contexto metodológico em que existe calçada.

O projeto não utiliza esses indicadores como uma certificação geral de acessibilidade de uma UF.

## 3. Primeira fonte complementar por Web Scraping

Como fonte complementar foi utilizado o levantamento do Mobilize Brasil:

**Calçadas do Brasil: notas em 228 locais.**

Script:

`02_data_acquisition_understanding/scraping_mobilize.py`

O script utiliza:

- Requests;
- BeautifulSoup;
- Pandas.

Os arquivos gerados são:

- `data/calcadas_mobilize.csv`;
- `data/calcadas_mobilize.txt`;
- `data/texto_mobilize.txt`.

## 4. Segunda página coletada por Web Scraping

Também foi utilizada a página:

**Panorama das calçadas.**

Script:

`02_data_acquisition_understanding/scraping_mobilize_panorama.py`

Essa coleta analisa parágrafos e itens de texto relacionados a categorias como:

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

Durante a coleta válida utilizada no desenvolvimento foram obtidos 17 trechos.

Arquivos gerados:

- `data/mobilize_panorama_calcadas.csv`;
- `data/mobilize_panorama_calcadas.txt`.

## 5. Tratamento da indisponibilidade do Mobilize

Durante o desenvolvimento foi observado que o site Mobilize pode responder com código HTTP 200 e, mesmo assim, apresentar internamente a mensagem:

`Esta página não pode ser exibida no momento`

Nesse caso, o código HTTP sozinho não é suficiente para considerar a coleta bem-sucedida.

Os dois scripts foram adaptados para verificar também o conteúdo recebido.

Quando a página está indisponível, o processo:

1. identifica a falha;
2. não sobrescreve os dados existentes;
3. mantém o último snapshot válido;
4. informa a situação no terminal;
5. evita gerar traceback desnecessário.

Na validação dessa contingência foram preservados:

- 228 registros da primeira coleta;
- 17 trechos da segunda coleta.

## 6. Visualização de frequência de termos

O arquivo:

`data/texto_mobilize.txt`

é utilizado para construir uma visualização de frequência de termos.

A aplicação utiliza os textos coletados para apresentar:

- tabela;
- gráfico de frequência.

A segunda fonte também permite visualizar a frequência das categorias encontradas.

## 7. Relação entre IBGE e Mobilize

IBGE e Mobilize tratam de alguns temas semelhantes, como:

- rampas;
- obstáculos;
- iluminação;
- arborização;
- condições das calçadas.

Entretanto, possuem metodologias, períodos, unidades de análise e escalas diferentes.

Por isso, os valores não são comparados numericamente de forma direta.

O Mobilize é utilizado como referência complementar ao conjunto de dados principal do IBGE.

## 8. Decisão sobre Selenium

Selenium foi avaliado durante o desenvolvimento.

Para as fontes selecionadas, não foi necessário utilizar automação de navegador porque, quando as páginas estão disponíveis, os dados podem ser obtidos diretamente do HTML utilizando Requests e BeautifulSoup.

A indisponibilidade temporária da fonte também não justifica utilizar Selenium apenas para tentar contornar uma falha do servidor.

## 9. API FastAPI

A aplicação possui uma API desenvolvida com FastAPI.

As principais rotas são:

- `GET /`;
- `GET /ufs`;
- `GET /ufs/{estado}`;
- `POST /observacoes`;
- `GET /observacoes`;
- `GET /ia/status`;
- `POST /ia/resumo-uf`.

## 10. Response Models

As respostas são estruturadas utilizando modelos Pydantic.

Na integração com IA foram definidos:

- `StatusIAResposta`;
- `ResumoUFEntrada`;
- `IndicadoresResumo`;
- `ResumoUFResposta`.

A rota:

`POST /ia/resumo-uf`

devolve:

- estado;
- região;
- modelo;
- dispositivo;
- indicadores;
- resumo produzido pelo LLM.

## 11. Integração com modelo de linguagem local

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente utilizando:

- PyTorch;
- Hugging Face Transformers;
- Hugging Face Hub.

Ambiente utilizado:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA não disponível.

Equipamento utilizado:

- Intel Core i7-1260P;
- aproximadamente 15,6 GB de RAM.

## 12. Utilização dos dados pelo LLM

O modelo não funciona como um chatbot genérico.

O usuário seleciona uma Unidade da Federação.

A FastAPI consulta a base e fornece ao modelo os seguintes indicadores:

- calçada/passeio;
- calçadas sem obstáculos;
- rampas;
- arborização.

O prompt orienta o modelo a:

- utilizar somente os dados fornecidos;
- não inventar valores;
- não utilizar informações externas;
- não classificar uma UF simplesmente como acessível ou inacessível;
- não interpretar os valores como percentual de todas as ruas;
- não criar um índice geral de acessibilidade;
- produzir um resumo curto em português do Brasil.

## 13. Tratamento de erros da API

Foram implementadas diferentes respostas HTTP.

### HTTP 404

Utilizado quando a Unidade da Federação solicitada não existe na base.

### HTTP 422

Utilizado quando os dados de entrada não passam pela validação do Pydantic.

### HTTP 503

Utilizado quando o modelo local não está disponível ou não pode ser executado.

### HTTP 500

Utilizado em uma falha inesperada durante a geração.

## 14. Integração com Streamlit

A página:

`pages/api_llm.py`

consome as respostas da FastAPI.

Os resultados não são apresentados apenas como JSON.

Eles são utilizados para alimentar:

- métricas;
- tabela;
- gráfico;
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
```

## 15. Dados complementares enviados pelo usuário

O Streamlit também permite upload de arquivos CSV.

O arquivo deve possuir a coluna:

`Estado`

As colunas adicionais podem ser associadas à base principal utilizando a Unidade da Federação como referência.

## 16. Documentação complementar

A justificativa da escolha do modelo está registrada em:

`03_modeling/escolha_modelo_tp4.md`

Os detalhes da integração estão registrados em:

`03_modeling/integracao_llm_tp4.md`

Repositório:

https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil