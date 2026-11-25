# Escolha do modelo local

## 1. Modelo selecionado

O modelo escolhido para o projeto foi:

`Qwen/Qwen2.5-0.5B-Instruct`

Ele é executado localmente utilizando a biblioteca Hugging Face Transformers, sem necessidade de uma API externa de Inteligência Artificial para gerar os textos.

A escolha considerou principalmente:

- possibilidade de execução no computador disponível;
- tamanho do modelo;
- capacidade de seguir instruções;
- suporte ao português;
- facilidade de integração com Python e Transformers;
- licença de uso;
- adequação às tarefas de geração e sumarização utilizadas no projeto.

---

## 2. Características do Qwen2.5-0.5B-Instruct

Segundo o model card oficial, o modelo possui aproximadamente:

`0,49 bilhão de parâmetros`

Ele é um modelo do tipo **Causal Language Model** ajustado para seguir instruções.

A família Qwen2.5 possui suporte multilíngue, incluindo português.

A licença informada para o modelo é:

`Apache 2.0`

Essas características permitem sua utilização no projeto acadêmico e sua execução com Hugging Face Transformers.

---

## 3. Por que utilizar um modelo pequeno

O projeto é executado em um computador pessoal sem GPU dedicada disponível para a aplicação.

O ambiente utilizado possui:

- Intel Core i7-1260P;
- aproximadamente 15,6 GB de memória RAM;
- execução em CPU;
- CUDA não disponível.

Por esse motivo, foi priorizado um modelo pequeno que pudesse ser executado localmente sem exigir infraestrutura especializada.

O objetivo da aplicação também não é manter uma conversa longa ou resolver tarefas gerais complexas.

O modelo é utilizado principalmente para:

- gerar análises curtas a partir de indicadores selecionados;
- resumir pequenos conjuntos de textos coletados por Web Scraping.

---

## 4. Teste local

O modelo foi executado localmente no equipamento utilizado no desenvolvimento.

Em teste anterior com geração de até 80 novos tokens foram observados:

- primeira geração: aproximadamente 9,48 segundos;
- segunda geração: aproximadamente 8,44 segundos.

A primeira execução também envolve o carregamento inicial do modelo.

O arquivo:

`llm_local.py`

utiliza cache para manter o modelo carregado em memória e reutilizá-lo nas próximas solicitações.

Esses testes demonstraram que o modelo escolhido pode ser executado no equipamento disponível utilizando somente CPU.

---

## 5. Comparação com Qwen2.5-1.5B-Instruct

Uma alternativa considerada é:

`Qwen/Qwen2.5-1.5B-Instruct`

Segundo o model card oficial, esse modelo possui aproximadamente:

`1,54 bilhão de parâmetros`

Assim como o modelo selecionado, ele pertence à família Qwen2.5, é ajustado para seguir instruções, possui suporte multilíngue incluindo português e utiliza licença:

`Apache 2.0`

A principal diferença relevante para este projeto é o tamanho.

O modelo de 1,5B possui um número de parâmetros consideravelmente maior que a versão de 0,5B.

Um modelo maior pode possuir maior capacidade para determinadas tarefas, mas também tende a exigir mais memória e processamento.

Neste projeto não foi realizado um benchmark direto entre as duas versões.

Por isso, não é correto afirmar que o modelo de 1,5B teria necessariamente melhor resultado nesta aplicação específica.

A escolha foi manter o Qwen2.5-0.5B-Instruct porque ele já foi instalado, integrado e testado no equipamento disponível, apresentando tempo de resposta compatível com a proposta acadêmica.

---

## 6. Comparação com FLAN-T5-base

Outra alternativa analisada foi:

`google/flan-t5-base`

O FLAN-T5 utiliza arquitetura diferente da família Qwen.

Enquanto o Qwen utilizado no projeto é um modelo causal de linguagem, o FLAN-T5 utiliza uma arquitetura do tipo **encoder-decoder**, normalmente utilizada com tarefas de transformação de texto para texto.

O model card oficial do FLAN-T5-base inclui o português entre os idiomas suportados.

Sua licença também é:

`Apache 2.0`

O FLAN-T5 seria uma alternativa possível para tarefas como sumarização e outras tarefas orientadas por instruções.

Entretanto, sua adoção exigiria alterar parte da implementação atual, que utiliza:

`AutoModelForCausalLM`

para trabalhar com o Qwen.

No FLAN-T5, a integração utiliza uma classe de modelo voltada a tarefas Seq2Seq.

Como o Qwen já estava integrado, testado localmente e funcionando com a arquitetura da aplicação, optou-se por manter a solução existente em vez de substituir o modelo apenas para a etapa final.

---

## 7. Comparação resumida

### Qwen2.5-0.5B-Instruct

- aproximadamente 0,49 bilhão de parâmetros;
- Causal Language Model;
- ajustado para seguir instruções;
- suporte ao português;
- licença Apache 2.0;
- executado e validado localmente no projeto;
- integração já implementada com `AutoModelForCausalLM`.

### Qwen2.5-1.5B-Instruct

- aproximadamente 1,54 bilhão de parâmetros;
- Causal Language Model;
- ajustado para seguir instruções;
- suporte ao português;
- licença Apache 2.0;
- maior que o modelo escolhido;
- não foi executado em benchmark local neste projeto.

### FLAN-T5-base

- arquitetura encoder-decoder;
- voltado a tarefas de texto para texto;
- suporta português;
- licença Apache 2.0;
- poderia ser utilizado para sumarização;
- exigiria adaptação da implementação atual;
- não foi executado em benchmark local neste projeto.

---

## 8. Limitações observadas no modelo escolhido

Os testes realizados na funcionalidade de sumarização mostraram uma limitação importante do Qwen2.5-0.5B-Instruct.

Mesmo utilizando instruções explícitas, o modelo em alguns testes realizou inferências que não estavam diretamente presentes nos textos utilizados como evidência.

Um exemplo observado foi transformar um item apresentado pela fonte como:

`existência de rampas de acessibilidade`

em uma afirmação sobre:

`falta de rampas`

Essa afirmação não estava sustentada pelo texto original.

Outro comportamento observado foi transformar critérios avaliados pelo levantamento em problemas efetivamente constatados.

Isso mostrou que o tamanho reduzido e a capacidade do modelo precisam ser considerados na aplicação.

---

## 9. Estratégia adotada para reduzir extrapolações

Em vez de aceitar automaticamente qualquer resposta do modelo, foi criada uma etapa de validação.

O funcionamento é:

```text
dados reais
    ↓
prompt
    ↓
Qwen
    ↓
validação da resposta
    ↓
resposta adequada?
   /          \
 sim          não
  ↓            ↓
resultado   nova tentativa
                ↓
          nova validação
                ↓
       ainda não adequada?
                ↓
         resumo de segurança
```

O resumo de segurança utiliza somente informações explicitamente presentes nas evidências fornecidas.

O Streamlit também informa ao usuário qual método foi utilizado.

Essa solução foi adotada porque o modelo deve apoiar a interpretação dos dados, e não substituir as fontes originais ou produzir informações sem evidência.

---

## 10. Engenharia de Prompt

O prompt utilizado na sumarização foi refinado durante os testes.

Entre as instruções estão:

- utilizar somente informações fornecidas;
- não acrescentar fatos externos;
- não transformar um critério avaliado em um problema constatado;
- não transformar existência de rampas em falta de rampas;
- evitar conclusões não presentes nos textos;
- não criar recomendações;
- limitar o tamanho da resposta;
- responder em português do Brasil.

O refinamento do prompt reduziu parte das respostas inadequadas, mas não eliminou completamente o problema.

Por isso, a Engenharia de Prompt foi combinada com a validação programática da saída.

---

## 11. Licença

O modelo escolhido:

`Qwen/Qwen2.5-0.5B-Instruct`

possui licença:

`Apache 2.0`

As duas alternativas consideradas neste documento também informam licença Apache 2.0 em seus respectivos model cards.

A licença foi considerada na escolha porque o modelo é baixado e executado localmente dentro da aplicação.

---

## 12. Decisão final

O Qwen2.5-0.5B-Instruct foi mantido porque apresenta uma combinação adequada para as condições deste projeto:

- pode ser executado no computador disponível;
- não exige GPU dedicada;
- possui suporte ao português;
- segue instruções;
- possui integração direta com Transformers;
- possui licença Apache 2.0;
- já foi testado localmente;
- já está integrado à FastAPI e ao Streamlit;
- permite executar a aplicação sem depender de uma API externa de IA.

A experiência prática também demonstrou que a escolha de um modelo pequeno possui limitações.

Por isso, a aplicação não depende exclusivamente da resposta do LLM e utiliza regras de Prompt Engineering, validação e transparência para reduzir o risco de apresentar informações não sustentadas pelos dados.

A escolha não significa que o Qwen2.5-0.5B-Instruct seja superior aos modelos alternativos.

Ela significa que, considerando o equipamento disponível, a arquitetura existente e o objetivo acadêmico do projeto, ele apresentou uma solução viável para a implementação local.

---

## 13. Fontes consultadas

- Hugging Face — `Qwen/Qwen2.5-0.5B-Instruct` — model card oficial.
- Hugging Face — `Qwen/Qwen2.5-1.5B-Instruct` — model card oficial.
- Hugging Face — `google/flan-t5-base` — model card oficial.