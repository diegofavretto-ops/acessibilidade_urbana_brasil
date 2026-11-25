# Integração do modelo de linguagem local

## 1. Modelo utilizado

O projeto utiliza o modelo:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente, sem utilização de uma API externa de Inteligência Artificial.

A justificativa da escolha, a licença e a comparação com modelos alternativos estão registradas em:

`03_modeling/escolha_modelo.md`

## 2. Ambiente utilizado

Durante o desenvolvimento foram utilizados:

- Python 3.14;
- PyTorch 2.15.0+cpu;
- Transformers 5.23.0;
- processador Intel Core i7-1260P;
- aproximadamente 15,6 GB de memória RAM;
- execução em CPU, sem CUDA.

O modelo está armazenado em:

`models/qwen2.5-0.5b-instruct`

A pasta `models/` está configurada no `.gitignore`, evitando o envio dos pesos do modelo ao GitHub.

## 3. Arquitetura da aplicação

A integração foi organizada de forma a separar as responsabilidades entre os arquivos.

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Navegação entre as páginas do Streamlit |
| `comum.py` | Funções compartilhadas de carregamento dos dados |
| `api.py` | Rotas, seleção dos dados, prompts e tratamento das respostas |
| `llm_local.py` | Carregamento e execução do modelo |
| `pages/api_llm.py` | Interface de consulta à API e análise dos indicadores |
| `pages/mobilize.py` | Análise dos dados do Mobilize e sumarização textual |
| `03_modeling/baixar_modelo.py` | Download do modelo |
| `03_modeling/testar_modelo_local.py` | Teste isolado do modelo |

Essa separação facilita a manutenção da aplicação e evita concentrar todas as funcionalidades em um único arquivo.

## 4. Carregamento do modelo

O arquivo `llm_local.py` concentra as principais funções relacionadas ao modelo:

- `carregar_tokenizer()`;
- `carregar_modelo()`;
- `obter_status_modelo()`;
- `gerar_resposta()`.

O carregamento utiliza o recurso `lru_cache`, da biblioteca padrão do Python.

Dessa forma, o modelo pode permanecer em memória e ser reutilizado nas próximas solicitações, evitando carregamentos desnecessários.

O modelo é utilizado apenas para inferência. Não é realizado treinamento ou fine-tuning.

## 5. Desempenho observado

Em um teste anterior com geração de até 80 novos tokens, foram registrados:

- primeira geração: 9,48 segundos;
- segunda geração: 8,44 segundos.

Esses resultados demonstraram a viabilidade da execução local no equipamento utilizado.

Os tempos não representam necessariamente o desempenho da sumarização dos textos do Mobilize, que utiliza prompts maiores e pode realizar mais de uma geração.

## 6. Integração com FastAPI

A FastAPI disponibiliza três rotas relacionadas à Inteligência Artificial.

### GET /ia/status

Permite consultar informações sobre o modelo e o dispositivo utilizado.

### POST /ia/resumo-uf

Recebe o nome de uma Unidade da Federação.

Exemplo:

`{"estado": "Santa Catarina"}`

A API consulta a base do IBGE e fornece ao modelo os indicadores de:

- existência de calçada ou passeio;
- calçadas sem obstáculos;
- presença de rampas;
- arborização.

O resultado é uma análise textual curta apresentada juntamente com os indicadores originais.

### POST /ia/resumo-mobilize

Recebe uma categoria relacionada aos textos coletados por Web Scraping.

Exemplo:

`{"categoria": "Rampas"}`

A API seleciona os textos correspondentes no arquivo:

`data/mobilize_panorama_calcadas.csv`

Os textos são inseridos no prompt e enviados ao modelo local para sumarização.

## 7. Sumarização automatizada

A sumarização dos textos coletados pelo Mobilize é a principal funcionalidade de geração textual da aplicação.

O usuário seleciona uma categoria no Streamlit e solicita uma síntese.

O processamento segue as seguintes etapas:

1. O Streamlit envia a categoria selecionada para a FastAPI.
2. A API consulta o arquivo CSV.
3. Os textos associados à categoria são selecionados.
4. Os textos são inseridos no prompt.
5. O Qwen executa a geração.
6. A resposta passa por uma verificação programática.
7. O resultado retorna para o Streamlit.
8. Os textos originais permanecem disponíveis para conferência.

## 8. Engenharia de Prompt

Os prompts fornecem ao modelo os dados necessários e instruções sobre como produzir as respostas.

Na sumarização textual, as principais orientações são:

- utilizar somente as evidências fornecidas;
- não inventar fatos externos;
- não transformar critérios avaliados em problemas constatados;
- não criar afirmações de ausência sem evidência;
- evitar recomendações não solicitadas;
- produzir uma resposta curta;
- utilizar português do Brasil.

Essa estratégia procura reduzir extrapolações e manter as respostas relacionadas aos dados reais do projeto.

## 9. Avaliação das respostas geradas

Durante os testes com a categoria Rampas, o modelo recebeu dois trechos coletados do Mobilize.

Uma das respostas apresentou a expressão:

> falta de rampas

Entretanto, o texto original apresentava a existência de rampas de acessibilidade como um dos critérios utilizados no levantamento.

A resposta do modelo transformou um critério de avaliação em uma condição negativa que não havia sido comprovada pelos textos.

Mesmo após o refinamento das instruções, foram observadas novas ocorrências desse comportamento.

Essa experiência demonstrou que a Engenharia de Prompt, isoladamente, não garante a fidelidade das respostas.

## 10. Verificação programática

Foi implementada no arquivo `api.py` uma função denominada:

`resumo_tem_extrapolacao()`

A função procura expressões previamente definidas que podem indicar interpretações inadequadas.

Quando uma dessas expressões é encontrada, o modelo recebe um novo prompt solicitando a correção da resposta.

A segunda resposta também passa pela mesma verificação.

Caso o problema continue, a aplicação utiliza a função:

`gerar_resumo_seguro()`

Essa função disponibiliza uma saída alternativa sem depender de uma nova geração do LLM.

Para a categoria Rampas, foi implementada uma síntese previamente construída com base nos dois trechos conhecidos.

Para as demais categorias, a saída alternativa informa a categoria e orienta o usuário a consultar os textos originais.

Essa verificação é baseada em expressões textuais e não constitui uma validação semântica completa. Portanto, ela pode reduzir determinadas extrapolações, mas não garante a identificação de todas as informações incorretas.

## 11. Transparência na apresentação dos resultados

A API retorna o campo:

`metodo_resumo`

Esse campo permite identificar três possibilidades:

- LLM — primeira resposta validada;
- LLM — resposta corrigida;
- Resumo de segurança baseado nas evidências.

Quando o resumo de segurança é utilizado, o Streamlit informa que a resposta do modelo não passou pela verificação implementada.

Dessa forma, o usuário consegue distinguir um texto produzido pelo LLM de uma saída alternativa construída pelo programa.

## 12. Resultado observado

No teste da categoria Rampas, a aplicação apresentou:

- categoria: Rampas;
- quantidade de trechos: 2;
- modelo: Qwen/Qwen2.5-0.5B-Instruct;
- dispositivo: CPU;
- método: Resumo de segurança baseado nas evidências.

A síntese apresentada foi:

> Os textos destacam a necessidade de calçadas de qualidade, com pavimentos bem nivelados, sem buracos e com rampas de acesso para cadeiras de rodas. O levantamento também considera critérios como irregularidades no piso, largura mínima, degraus, obstáculos, rampas de acessibilidade, iluminação, sinalização e paisagismo.

Esse resultado demonstra o funcionamento da estratégia alternativa e da identificação do método utilizado.

O texto apresentado nesse teste não foi gerado diretamente pelo LLM, pois suas respostas anteriores não passaram pela verificação programática.

## 13. Validação com Pydantic

As entradas e respostas da API utilizam modelos Pydantic.

Entre os modelos utilizados estão:

- `StatusIAResposta`;
- `ResumoUFEntrada`;
- `IndicadoresResumo`;
- `ResumoUFResposta`;
- `ResumoMobilizeEntrada`;
- `ResumoMobilizeResposta`.

O Pydantic verifica a estrutura e os tipos dos dados.

Essa validação estrutural é diferente da verificação do conteúdo textual produzido pelo modelo.

## 14. Tratamento de erros

A API utiliza códigos HTTP para identificar diferentes situações:

- **200:** solicitação processada com sucesso;
- **404:** UF ou categoria não encontrada;
- **422:** dados de entrada inválidos;
- **503:** modelo ou dados necessários indisponíveis, incluindo determinadas falhas de execução;
- **500:** falha inesperada durante o processamento.

O Streamlit apresenta mensagens correspondentes para orientar o usuário.

## 15. Execução da aplicação

Para iniciar a FastAPI, executar na raiz do projeto:

```powershell
python -m uvicorn api:app
```

A documentação automática está disponível em:

http://127.0.0.1:8000/docs

Em outro terminal, iniciar o Streamlit:

```powershell
python -m streamlit run app.py
```

O dashboard está disponível em:

http://localhost:8501

Os dois processos devem estar em execução para utilizar as funcionalidades integradas de Inteligência Artificial.

## 16. Limitações e possibilidades de melhoria

O modelo escolhido possui tamanho reduzido e pode apresentar dificuldades de interpretação, mesmo quando recebe instruções específicas.

A verificação implementada procura identificar determinadas expressões, mas não substitui uma avaliação humana da fidelidade da resposta.

A síntese alternativa da categoria Rampas também depende dos textos conhecidos no momento do desenvolvimento e deverá ser revisada caso a fonte seja atualizada.

Como possibilidades de melhoria, podem ser considerados:

- avaliação de modelos com maior capacidade;
- comparação experimental entre modelos;
- ampliação dos testes para diferentes categorias;
- aprimoramento da verificação de fidelidade;
- desenvolvimento de uma sumarização extrativa automática como alternativa ao LLM.

Essas melhorias não fazem parte da implementação atual.

## 17. Conclusão

A aplicação integra dados reais, Web Scraping, Python, Pandas, FastAPI, Streamlit e um modelo de linguagem executado localmente.

Além da integração tecnológica, os testes permitiram identificar limitações práticas da geração de textos por um LLM pequeno.

A Engenharia de Prompt e a verificação programática foram utilizadas para reduzir determinadas extrapolações, preservando os dados e textos originais como principais referências para interpretação dos resultados.