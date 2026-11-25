# Data Summary Report

## 1. Objetivo deste documento

Este documento resume as fontes de dados utilizadas no projeto **Acessibilidade Urbana no Brasil**, a forma como os dados são coletados e tratados e como são utilizados nas etapas de análise, visualização e Inteligência Artificial.

O projeto utiliza uma fonte quantitativa principal do IBGE e duas fontes complementares obtidas por Web Scraping no Mobilize Brasil.

Os conjuntos possuem metodologias e unidades de análise diferentes e, por isso, são utilizados de forma complementar.

---

## 2. Fonte quantitativa principal

A principal fonte quantitativa utilizada é:

**IBGE — Censo Demográfico 2022 — Características Urbanísticas do Entorno dos Domicílios — Tabela SIDRA 9584.**

Os dados foram organizados por Unidade da Federação para utilização:

- no dashboard Streamlit;
- nas comparações entre UFs;
- nas comparações entre regiões;
- na FastAPI;
- na geração de análises textuais com o modelo local.

A base utilizada na aplicação está armazenada em:

`02_data_acquisition_understanding/ufs_streamlit_resumo.csv`

Foram consideradas as 27 Unidades da Federação.

---

## 3. Campos utilizados do IBGE

Os principais campos da base são:

| Campo | Tipo | Finalidade |
|---|---|---|
| Estado | String | Identificação da Unidade da Federação |
| Regiao | String | Identificação da região brasileira |
| Domicilios_base | Integer | Quantidade de domicílios utilizada como referência |
| Iluminacao_publica_pct | Float | Existência de iluminação pública no entorno |
| Ponto_onibus_van_pct | Float | Existência de ponto de ônibus ou van |
| Via_bicicleta_pct | Float | Existência de infraestrutura para bicicleta |
| Calcada_passeio_pct | Float | Existência de calçada ou passeio |
| Calcadas_sem_obstaculos_pct | Float | Calçadas sem obstáculos |
| Rampas_pct | Float | Presença de rampas |
| Arborizacao_com_arvores_pct | Float | Presença de arborização com árvores |

Os percentuais representam características observadas no entorno dos domicílios considerados na pesquisa.

Eles não devem ser interpretados diretamente como percentual de todas as ruas de uma Unidade da Federação.

Os indicadores de rampas e de calçadas sem obstáculos também precisam ser interpretados dentro do contexto metodológico em que existe calçada.

O projeto não utiliza esses indicadores como certificação geral de acessibilidade de uma UF.

---

## 4. Primeira fonte complementar por Web Scraping

A primeira fonte complementar utilizada é o levantamento do Mobilize Brasil:

**Calçadas do Brasil: notas em 228 locais.**

O script utilizado é:

`02_data_acquisition_understanding/scraping_mobilize.py`

A coleta utiliza:

- Requests;
- BeautifulSoup;
- Pandas.

Os principais arquivos gerados são:

- `data/calcadas_mobilize.csv`;
- `data/calcadas_mobilize.txt`;
- `data/texto_mobilize.txt`.

Essa fonte apresenta avaliações numéricas relacionadas a critérios das calçadas.

Entre os critérios utilizados estão:

- irregularidades;
- degraus;
- inclinação;
- largura;
- rampas;
- obstáculos;
- iluminação;
- arborização;
- sinalização.

As avaliações são apresentadas em escala de 0 a 10.

---

## 5. Segunda fonte complementar por Web Scraping

A segunda página utilizada é:

**Panorama das Calçadas — Mobilize Brasil.**

O script utilizado é:

`02_data_acquisition_understanding/scraping_mobilize_panorama.py`

Essa coleta é voltada para conteúdo textual.

Durante a coleta válida utilizada no projeto foram obtidos **17 trechos de texto**.

Os trechos foram classificados em categorias como:

- Calçadas;
- Degraus;
- Iluminação;
- Irregularidades;
- Largura;
- Obstáculos;
- Paisagismo;
- Pedestres;
- Rampas;
- Sinalização.

Os arquivos gerados são:

- `data/mobilize_panorama_calcadas.csv`;
- `data/mobilize_panorama_calcadas.txt`.

O arquivo CSV contém campos como:

- ordem;
- categorias;
- texto;
- fonte;
- URL.

---

## 6. Tratamento de indisponibilidade do Mobilize

Durante o desenvolvimento foi observado que o site Mobilize pode responder com código HTTP 200 e, mesmo assim, apresentar uma página interna com a mensagem:

`Esta página não pode ser exibida no momento`

Por isso, o código HTTP 200 isoladamente não é considerado suficiente para confirmar que a coleta foi válida.

Os scripts verificam também o conteúdo da página.

Quando a fonte está indisponível, o processo:

1. identifica a situação;
2. evita sobrescrever os arquivos existentes;
3. preserva o último snapshot válido;
4. informa a ocorrência no terminal;
5. evita interromper o processo com traceback desnecessário.

Nos testes dessa contingência foram preservados:

- 228 registros da primeira coleta;
- 17 trechos da segunda coleta.

---

## 7. Tratamento dos dados

O tratamento dos dados é realizado principalmente com Python e Pandas.

Entre as operações utilizadas estão:

- leitura de arquivos CSV;
- seleção de colunas;
- conversão de valores;
- cálculo de médias;
- ordenação;
- filtragem;
- agrupamentos;
- comparação entre Unidades da Federação;
- comparação entre regiões;
- remoção de duplicidades;
- separação de categorias;
- contagem de termos;
- contagem de categorias.

Na análise textual também são removidas palavras muito comuns que pouco contribuem para a interpretação dos temas.

---

## 8. Uso dos dados no dashboard

O Streamlit apresenta os dados de diferentes formas.

Entre as funcionalidades estão:

- ranking nacional;
- consulta de uma Unidade da Federação;
- comparação entre UFs;
- comparação entre regiões;
- métricas;
- tabelas;
- gráficos;
- dados complementares do Mobilize;
- frequência de termos;
- frequência de categorias;
- textos obtidos por Web Scraping;
- integração com FastAPI;
- análises geradas com modelo de linguagem local;
- sumarização de textos com IA.

O objetivo é transformar os dados brutos em informações mais fáceis de consultar e interpretar.

---

## 9. Relação entre os dados do IBGE e Mobilize

IBGE e Mobilize abordam alguns temas semelhantes, como:

- condições das calçadas;
- rampas;
- obstáculos;
- iluminação;
- arborização.

Entretanto, as duas fontes possuem:

- metodologias diferentes;
- períodos diferentes;
- unidades de análise diferentes;
- formas diferentes de coleta.

Por isso, os valores não são comparados numericamente de forma direta.

O IBGE é utilizado como fonte quantitativa principal.

O Mobilize é utilizado como fonte complementar para ampliar a análise sobre o ambiente urbano e as condições das calçadas.

---

## 10. Decisão sobre Selenium

A necessidade de utilizar Selenium foi avaliada.

Para as fontes selecionadas, quando as páginas estão disponíveis, as informações necessárias podem ser obtidas diretamente do HTML com Requests e BeautifulSoup.

Não foi identificada necessidade de:

- executar cliques;
- preencher formulários;
- aguardar conteúdo obrigatório carregado por JavaScript;
- controlar um navegador.

Por esse motivo, foi mantida a solução mais simples com Requests e BeautifulSoup.

---

## 11. API FastAPI

O projeto possui uma API desenvolvida com FastAPI.

As principais rotas são:

- `GET /`;
- `GET /ufs`;
- `GET /ufs/{estado}`;
- `POST /observacoes`;
- `GET /observacoes`;
- `GET /ia/status`;
- `POST /ia/resumo-uf`;
- `POST /ia/resumo-mobilize`.

A documentação automática pode ser acessada localmente em:

`http://127.0.0.1:8000/docs`

---

## 12. Uso do Pydantic

A FastAPI utiliza modelos Pydantic para definir a estrutura dos dados de entrada e saída.

Entre os modelos utilizados estão:

- `StatusIAResposta`;
- `ResumoUFEntrada`;
- `IndicadoresResumo`;
- `ResumoUFResposta`;
- `ResumoMobilizeEntrada`;
- `ResumoMobilizeResposta`.

O Pydantic ajuda a validar se os dados enviados para a API possuem a estrutura esperada.

---

## 13. Modelo de linguagem local

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente com:

- PyTorch;
- Hugging Face Transformers.

O projeto utiliza o modelo apenas para inferência.

Não é realizado treinamento nem fine-tuning.

O carregamento principal do modelo está isolado no arquivo:

`llm_local.py`

O arquivo utiliza cache para evitar carregar novamente o modelo a cada solicitação.

---

## 14. Ambiente utilizado para o LLM

Durante os testes foram utilizados:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- execução em CPU;
- CUDA não disponível.

Equipamento utilizado:

- Intel Core i7-1260P;
- aproximadamente 15,6 GB de memória RAM.

Em testes anteriores com geração de até 80 novos tokens foram observados aproximadamente:

- 9,48 segundos na primeira geração;
- 8,44 segundos na segunda geração.

A diferença ocorre porque o modelo permanece carregado em memória após a primeira utilização.

---

## 15. Primeira utilização do LLM — indicadores do IBGE

A rota:

`POST /ia/resumo-uf`

recebe uma Unidade da Federação.

A API consulta os dados do IBGE e fornece ao modelo indicadores relacionados a:

- calçada ou passeio;
- calçadas sem obstáculos;
- rampas;
- arborização.

O prompt orienta o modelo a:

- utilizar somente os dados fornecidos;
- não inventar valores;
- não utilizar informações externas;
- não classificar uma UF simplesmente como acessível ou inacessível;
- não interpretar os percentuais como percentual de todas as ruas;
- não criar um índice geral de acessibilidade;
- produzir uma análise curta em português do Brasil.

---

## 16. Sumarização automatizada dos textos do Mobilize

A funcionalidade principal de IA utilizada na etapa final é a **sumarização automatizada de textos**.

A rota utilizada é:

`POST /ia/resumo-mobilize`

Exemplo de entrada:

```json
{
  "categoria": "Rampas"
}
```

A API procura os trechos coletados pelo Web Scraping associados à categoria selecionada.

Em seguida, esses textos são incluídos no prompt enviado ao Qwen.

O fluxo é:

```text
Web Scraping
    ↓
CSV com textos do Mobilize
    ↓
seleção da categoria
    ↓
FastAPI
    ↓
trechos correspondentes
    ↓
prompt
    ↓
Qwen local
    ↓
validação
    ↓
Streamlit
```

---

## 17. Engenharia de Prompt

O prompt utilizado na sumarização possui regras para diminuir extrapolações.

Entre as instruções estão:

- utilizar apenas informações presentes nos textos fornecidos;
- não acrescentar fatos externos;
- não transformar um critério avaliado em um problema constatado;
- não transformar a existência de rampas em falta de rampas;
- não criar ausências ou deficiências que não estejam explicitamente descritas;
- evitar recomendações;
- limitar o tamanho do texto;
- escrever em português do Brasil.

Durante os testes, o modelo apresentou respostas que, apesar de linguisticamente corretas, faziam interpretações que não estavam sustentadas pelos textos.

Um exemplo observado foi transformar a expressão:

`existência de rampas de acessibilidade`

em:

`falta de rampas`

Essa diferença mostrou a necessidade de validar a saída do modelo antes de apresentá-la ao usuário.

---

## 18. Validação da resposta do LLM

A aplicação utiliza uma etapa adicional após a geração do texto.

O fluxo é:

```text
Qwen gera resposta
        ↓
verificação da resposta
        ↓
há expressão suspeita?
      /       \
    não       sim
     ↓         ↓
resultado   nova tentativa
               ↓
          nova validação
               ↓
        resposta ainda inadequada?
               ↓
       resumo de segurança
```

A primeira resposta do modelo é analisada em busca de algumas expressões que podem representar extrapolação.

Se uma dessas situações for identificada, é realizada uma segunda geração com instruções mais restritivas.

Se a segunda resposta ainda apresentar o mesmo tipo de problema, a aplicação utiliza um resumo de segurança construído somente com informações explicitamente presentes nos textos coletados.

---

## 19. Transparência da sumarização

O Streamlit informa ao usuário qual método foi utilizado.

Os possíveis resultados incluem:

- `LLM - primeira resposta validada`;
- `LLM - resposta corrigida`;
- `Resumo de segurança baseado nas evidências`.

Quando é utilizado o resumo de segurança, a interface informa explicitamente que a resposta do modelo não passou pela validação de fidelidade.

Dessa forma, um texto de segurança não é apresentado como se tivesse sido uma resposta validada do LLM.

Os trechos originais utilizados na análise também permanecem disponíveis para conferência.

---

## 20. Tratamento de erros da API

Foram implementadas respostas HTTP diferentes para situações distintas.

### HTTP 404

Utilizado quando:

- uma UF não existe na base;
- uma categoria do Mobilize não é encontrada.

### HTTP 422

Utilizado quando os dados enviados não passam pela validação do Pydantic.

### HTTP 503

Utilizado quando:

- o modelo local não está disponível;
- um arquivo necessário não está disponível;
- ocorre uma falha relacionada à disponibilidade do modelo ou dos dados.

### HTTP 500

Utilizado para falhas inesperadas durante o processamento.

---

## 21. Integração com Streamlit

A integração ocorre principalmente nas páginas:

`pages/api_llm.py`

e:

`pages/mobilize.py`

A página relacionada ao Mobilize permite:

- visualizar dados coletados por Web Scraping;
- selecionar critérios;
- observar rankings;
- analisar médias;
- visualizar termos recorrentes;
- visualizar categorias;
- consultar os textos originais;
- selecionar uma categoria;
- solicitar uma síntese;
- visualizar o modelo utilizado;
- visualizar o dispositivo de execução;
- verificar o método de síntese;
- consultar os textos utilizados como evidência.

---

## 22. Fluxo completo do projeto

O ciclo utilizado pode ser resumido da seguinte forma:

```text
IBGE + Mobilize
       ↓
aquisição dos dados
       ↓
tratamento com Python/Pandas
       ↓
análise e organização
       ↓
FastAPI
       ↓
Prompt Engineering + Qwen
       ↓
validação da saída
       ↓
Streamlit
       ↓
visualizações e sínteses
```

Esse fluxo reúne aquisição, tratamento, análise, modelagem e apresentação dos resultados.

---

## 23. Relação com ODS e ESG

O projeto está relacionado ao:

**ODS 11 — Cidades e Comunidades Sustentáveis.**

Os dados analisados envolvem temas relacionados ao ambiente urbano, mobilidade de pedestres, calçadas, rampas, obstáculos e arborização.

No enquadramento acadêmico do projeto, a acessibilidade urbana também possui relação principalmente com a dimensão **Social (S)** do ESG.

Essa relação é uma interpretação utilizada no projeto e não uma classificação produzida pelo IBGE ou pelo Mobilize.

---

## 24. Limitações

Entre as limitações do projeto estão:

- diferenças metodológicas entre IBGE e Mobilize;
- impossibilidade de interpretar os percentuais do IBGE como percentual de todas as ruas;
- número limitado de textos coletados no Panorama das Calçadas;
- indisponibilidade temporária do site Mobilize;
- execução do modelo em CPU;
- limitações de interpretação do Qwen2.5-0.5B-Instruct;
- possibilidade de o LLM gerar inferências não sustentadas pelos textos.

A validação adicionada à aplicação reduz parte desse risco, mas não transforma o modelo em uma fonte de verdade.

Os textos originais e os dados devem permanecer como referência principal.

---

## 25. Repositório

O projeto está disponível em:

`https://github.com/diegofavretto-ops/acessibilidade_urbana_brasil`