# Engenharia de Prompt

## 1. Objetivo

A Engenharia de Prompt foi utilizada no projeto Acessibilidade Urbana no Brasil para orientar o modelo de linguagem na geração de respostas relacionadas aos dados reais da aplicação.

O objetivo é produzir análises e sínteses textuais que auxiliem o usuário na interpretação das informações, reduzindo o risco de respostas que não estejam sustentadas pelos dados fornecidos.

## 2. Modelo utilizado

O modelo utilizado é:

`Qwen/Qwen2.5-0.5B-Instruct`

O modelo é executado localmente com Hugging Face Transformers e PyTorch.

Não foi realizado treinamento ou fine-tuning. As respostas são orientadas por instruções fornecidas no momento da inferência.

## 3. Estrutura dos prompts

Os prompts foram organizados considerando os seguintes elementos:

- definição da tarefa;
- contexto da solicitação;
- fornecimento dos dados;
- instruções e restrições;
- definição do formato esperado da resposta.

Essa estrutura permite informar ao modelo não apenas o que deve ser produzido, mas também quais informações podem ser utilizadas e quais interpretações devem ser evitadas.

## 4. Prompt para análise dos indicadores do IBGE

A primeira funcionalidade utiliza os indicadores de uma Unidade da Federação para gerar uma análise textual.

A API seleciona os dados relacionados a:

- existência de calçada ou passeio;
- calçadas sem obstáculos;
- presença de rampas;
- arborização.

O prompt fornece esses valores ao modelo e estabelece regras para sua interpretação.

Entre as principais restrições estão:

- utilizar somente os dados fornecidos;
- não inventar valores;
- não acrescentar informações externas;
- não classificar a UF como acessível ou inacessível;
- não interpretar os percentuais como percentual de todas as ruas;
- não criar um índice geral de acessibilidade;
- produzir uma análise curta em português do Brasil.

A funcionalidade é disponibilizada pela rota:

`POST /ia/resumo-uf`

## 5. Prompt para sumarização dos textos do Mobilize

A segunda funcionalidade utiliza textos reais obtidos por Web Scraping.

O usuário seleciona uma categoria no Streamlit.

A FastAPI localiza os trechos correspondentes no arquivo:

`data/mobilize_panorama_calcadas.csv`

Os textos encontrados são inseridos dinamicamente no prompt.

A funcionalidade é disponibilizada pela rota:

`POST /ia/resumo-mobilize`

## 6. Construção dinâmica do prompt

O prompt não contém um texto fixo para todas as categorias.

As informações variam de acordo com a escolha do usuário.

A categoria selecionada e os textos recuperados são inseridos utilizando f-strings do Python.

Exemplo simplificado:

```python
prompt = f"""
TAREFA:
Produza uma síntese fiel aos textos fornecidos.

CATEGORIA:
{categoria}

EVIDÊNCIAS:
{textos_numerados}

REGRAS:
Utilize somente as informações fornecidas.
Não acrescente fatos externos.
Produza uma resposta curta em português.

RESPOSTA:
"""
```

Esse exemplo apresenta uma versão simplificada da estrutura. O prompt completo utilizado pela aplicação está implementado no arquivo `api.py`.

A utilização de f-strings permite reutilizar a mesma estrutura de instruções para diferentes categorias e conjuntos de textos.

## 7. Refinamento dos prompts

Durante o desenvolvimento foram realizados testes com a categoria Rampas, que possui dois trechos associados na base utilizada.

Os resultados permitiram observar diferentes comportamentos do modelo.

### Primeiro teste

A resposta foi extensa, apresentou uma introdução desnecessária e terminou sem concluir adequadamente a última frase.

Também apresentou referências separadas ao texto 1 e ao texto 2.

### Segundo teste

Foram acrescentadas instruções para limitar a resposta a duas frases e evitar introduções, títulos e listas.

O resultado ficou mais curto, porém apresentou uma conclusão sobre a implementação eficaz de caminhos seguros e acessíveis que não estava explicitamente registrada nos textos fornecidos.

### Terceiro teste

Foram acrescentadas restrições para evitar conclusões externas e diferenciar critérios avaliados de problemas efetivamente constatados.

Mesmo assim, o modelo utilizou a expressão:

`falta de rampas de acesso`

O texto original informava que a existência de rampas era um dos critérios utilizados na avaliação.

Portanto, a resposta apresentou uma interpretação que não estava sustentada pelas evidências.

### Quarto teste

Foi implementada uma verificação programática da resposta, com uma segunda tentativa de geração quando determinadas expressões fossem identificadas.

Entretanto, durante o teste realizado, a segunda resposta continuou apresentando interpretações inadequadas.

### Solução implementada

Foi acrescentada uma saída alternativa para situações em que as duas respostas geradas apresentassem expressões consideradas problemáticas.

Essa saída é identificada na interface como resumo de segurança.

## 8. Verificação programática

A função `resumo_tem_extrapolacao()` verifica a presença de determinadas expressões na resposta do modelo.

Entre os exemplos estão:

- falta de rampas;
- ausência de rampas;
- problemas de calçadas;
- irregularidades na infraestrutura;
- deficiências encontradas.

A verificação foi construída a partir dos problemas observados durante os testes.

O fluxo implementado é:

```text
Construção do prompt
        |
Geração pelo Qwen
        |
Verificação de expressões
        |
Nova tentativa, se necessário
        |
Segunda verificação
        |
Apresentação do resultado
ou utilização da saída alternativa
```

Essa estratégia combina Engenharia de Prompt com regras implementadas em Python.

A verificação é baseada na presença de expressões específicas. Ela não constitui uma avaliação semântica completa e não garante a identificação de todas as possíveis extrapolações.

## 9. Prompt de correção

Quando a primeira resposta apresenta uma das expressões verificadas, a API constrói um segundo prompt.

Esse prompt inclui:

- os textos originais;
- a resposta anterior;
- uma instrução solicitando sua correção;
- regras adicionais para evitar as interpretações identificadas.

O modelo recebe uma nova oportunidade de produzir uma resposta mais adequada.

Essa abordagem pode ser entendida como um processo de refinamento da geração.

## 10. Saída alternativa

Caso a segunda resposta também apresente expressões consideradas problemáticas, o sistema utiliza a função:

`gerar_resumo_seguro()`

Para a categoria Rampas, essa função retorna um texto previamente elaborado com base nos dois trechos conhecidos.

Para as demais categorias, a função apresenta uma mensagem conservadora, indicando a categoria selecionada e orientando a consulta aos textos originais.

Essa saída alternativa não é uma nova geração do LLM.

A aplicação informa ao usuário quando esse mecanismo é utilizado.

## 11. Resultado observado

No teste final da categoria Rampas, o sistema apresentou:

- quantidade de trechos utilizados: 2;
- modelo consultado: Qwen/Qwen2.5-0.5B-Instruct;
- dispositivo: CPU;
- método: Resumo de segurança baseado nas evidências.

A interface também informou que a resposta do modelo não passou pela verificação de fidelidade implementada.

O teste demonstrou o funcionamento do mecanismo de contingência e da identificação da origem do texto apresentado.

## 12. Transparência e rastreabilidade

A aplicação mantém disponíveis os textos originais utilizados como evidência.

O usuário pode comparar a síntese apresentada com o conteúdo coletado.

Além disso, o campo `metodo_resumo` informa se o resultado corresponde a:

- primeira resposta do LLM aceita pela verificação;
- resposta corrigida do LLM;
- resumo de segurança.

Essa distinção evita atribuir ao modelo um texto que foi produzido por uma regra do programa.

## 13. Limitações

Os testes mostraram que um modelo pequeno pode produzir respostas inadequadas mesmo quando recebe instruções específicas.

O refinamento dos prompts não eliminou completamente as extrapolações observadas.

A verificação por expressões também apresenta limitações, pois uma afirmação incorreta pode ser formulada de maneiras não previstas pelo programa.

A saída alternativa específica de Rampas foi elaborada com base nos textos existentes durante o desenvolvimento e deverá ser revisada caso essas evidências sejam modificadas.

Por esses motivos, os dados e textos originais permanecem como a principal referência para interpretação dos resultados.

## 14. Relação com o ODS 11

A Engenharia de Prompt foi aplicada para apoiar a interpretação de informações relacionadas às condições das calçadas e à acessibilidade urbana.

Esses temas estão relacionados ao ODS 11 — Cidades e Comunidades Sustentáveis.

A utilização da Inteligência Artificial procura facilitar o acesso às informações, sem substituir a análise técnica ou alterar o significado das fontes originais.

## 15. Conclusão

A Engenharia de Prompt permitiu orientar a geração de análises e sínteses a partir dos dados reais da aplicação.

Os testes também demonstraram que fornecer boas instruções ao modelo não é suficiente para garantir respostas sempre corretas.

Por esse motivo, foram combinados prompts estruturados, refinamento das instruções, verificação programática, mecanismos de contingência e apresentação das evidências originais.

A experiência permitiu compreender tanto as possibilidades quanto as limitações práticas da utilização de modelos de linguagem em aplicações de Ciência de Dados.