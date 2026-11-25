# Modeling Report

## 1. Objetivo da modelagem

A etapa de modelagem do projeto Acessibilidade Urbana no Brasil tem como objetivo utilizar técnicas de análise de dados e Inteligência Artificial para facilitar a interpretação das informações relacionadas às condições do entorno urbano.

A proposta combina análise exploratória de dados com um modelo de linguagem executado localmente.

Não foi desenvolvido um modelo de previsão ou classificação, pois o problema definido está relacionado principalmente à consulta, comparação e interpretação das informações disponíveis.

## 2. Dados utilizados

A modelagem utiliza duas fontes principais de informação:

- indicadores quantitativos do Censo Demográfico 2022 do IBGE;
- informações complementares coletadas por Web Scraping no Mobilize Brasil.

Os dados quantitativos permitem comparar indicadores entre Unidades da Federação e regiões brasileiras.

Os dados textuais permitem analisar conteúdos relacionados às condições das calçadas e realizar sumarização automatizada.

## 3. Análise exploratória

Antes da integração com Inteligência Artificial, foram desenvolvidas análises utilizando Python e Pandas.

Entre as principais operações realizadas estão:

- cálculo de médias;
- ordenação de indicadores;
- rankings;
- comparação entre Unidades da Federação;
- comparação entre regiões;
- frequência de palavras;
- frequência de categorias;
- filtragem de textos.

Essas análises são apresentadas no Streamlit por meio de métricas, tabelas, gráficos e seletores interativos.

## 4. Modelo selecionado

O modelo escolhido foi:

`Qwen/Qwen2.5-0.5B-Instruct`

A escolha considerou a possibilidade de execução em CPU, o tamanho reduzido do modelo, o suporte ao português e a integração com Hugging Face Transformers.

Também foram consideradas duas alternativas:

- Qwen2.5-1.5B-Instruct;
- FLAN-T5-base.

A comparação detalhada e as informações sobre as licenças estão disponíveis no documento `escolha_modelo.md`.

## 5. Metodologia

O modelo é utilizado para inferência, sem treinamento ou fine-tuning.

Foram implementadas duas funcionalidades:

### Análise de indicadores do IBGE

O usuário seleciona uma Unidade da Federação.

A aplicação recupera quatro indicadores da base e fornece essas informações ao modelo por meio de um prompt estruturado.

A finalidade é apresentar uma análise textual complementar aos dados numéricos.

### Sumarização dos textos do Mobilize

O usuário seleciona uma categoria relacionada às condições das calçadas.

A aplicação recupera os textos associados à categoria e solicita ao modelo a produção de uma síntese.

Os textos originais permanecem disponíveis para conferência.

## 6. Engenharia de Prompt

Os prompts foram desenvolvidos para orientar o modelo quanto à tarefa, aos dados disponíveis, às restrições e ao formato esperado da resposta.

Durante o desenvolvimento foram realizados refinamentos com base nos resultados observados.

As principais orientações foram:

- utilizar somente as informações fornecidas;
- evitar dados e conclusões externas;
- respeitar o contexto metodológico das fontes;
- não transformar critérios avaliados em problemas constatados;
- produzir textos curtos em português do Brasil.

Os testes e refinamentos estão documentados em `prompt_engineering.md`.

## 7. Avaliação do modelo

A avaliação realizada foi principalmente qualitativa, considerando a comparação entre as respostas produzidas pelo modelo e os textos originais.

Foram considerados os seguintes critérios:

- fidelidade às informações fornecidas;
- relevância para a categoria selecionada;
- clareza do texto;
- ausência de informações inventadas;
- adequação ao formato solicitado;
- conclusão adequada da resposta.

Não foram calculadas métricas quantitativas de sumarização, como ROUGE, nem realizado um benchmark experimental entre diferentes modelos.

## 8. Resultados observados

O modelo foi executado localmente em um computador com processador Intel Core i7-1260P e aproximadamente 15,6 GB de memória RAM.

Em um teste anterior com geração de até 80 novos tokens, foram observados os seguintes tempos:

- primeira geração: 9,48 segundos;
- segunda geração: 8,44 segundos.

Esses resultados demonstraram a viabilidade da execução local utilizando CPU.

Nos testes de sumarização da categoria Rampas, entretanto, foram observadas dificuldades relacionadas à interpretação dos textos.

O modelo transformou a existência de rampas como critério de avaliação em uma afirmação sobre falta de rampas, que não estava sustentada pelas evidências fornecidas.

## 9. Estratégia de contingência

Para reduzir a apresentação de determinadas extrapolações, foi implementada uma verificação programática das respostas.

Quando são identificadas expressões previamente definidas como problemáticas, o modelo recebe uma segunda solicitação de geração.

Se a segunda resposta também apresentar essas expressões, a aplicação utiliza uma saída alternativa.

No teste da categoria Rampas, o mecanismo de contingência foi acionado corretamente.

A interface informou que o resultado apresentado correspondia a um resumo de segurança, e não a uma resposta do LLM aceita pela verificação.

Esse mecanismo não constitui uma validação semântica completa e não elimina todas as possibilidades de erro.

## 10. Integração com a aplicação

A modelagem está integrada à FastAPI e ao Streamlit.

As principais responsabilidades estão distribuídas entre:

- `llm_local.py`: carregamento e execução do modelo;
- `api.py`: recuperação dos dados, construção dos prompts e tratamento das respostas;
- `pages/api_llm.py`: apresentação dos indicadores e análises textuais;
- `pages/mobilize.py`: análise das informações coletadas e sumarização de textos.

Essa organização permite separar as funcionalidades de processamento, geração e apresentação.

## 11. Relação com o ODS 11 e ESG

A modelagem procura facilitar a interpretação de informações relacionadas à acessibilidade urbana, às condições das calçadas e à mobilidade de pedestres.

Esses temas estão relacionados ao ODS 11 — Cidades e Comunidades Sustentáveis.

No enquadramento acadêmico do projeto, também apresentam relação principalmente com a dimensão Social do ESG.

A aplicação pode auxiliar na consulta de informações relevantes para o planejamento urbano, sem substituir avaliações técnicas especializadas.

## 12. Limitações

As principais limitações identificadas são:

- capacidade reduzida de interpretação do modelo escolhido;
- possibilidade de extrapolações nas respostas;
- quantidade limitada de textos coletados;
- diferenças metodológicas entre as fontes;
- execução em CPU;
- ausência de comparação experimental entre modelos;
- verificação de respostas baseada em expressões específicas.

A avaliação realizada não permite afirmar que o modelo produz sínteses corretas para todas as categorias disponíveis.

## 13. Conclusão

A etapa de modelagem permitiu integrar técnicas de análise exploratória e Inteligência Artificial aos dados reais utilizados no projeto.

Os testes demonstraram a viabilidade técnica da execução local e da integração entre o modelo, a API e o dashboard.

Também permitiram identificar limitações práticas do modelo e implementar mecanismos de contingência e transparência.

A Inteligência Artificial é utilizada como ferramenta complementar de interpretação, mantendo os dados originais como principal referência para a análise.